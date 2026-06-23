(function () {
    "use strict";

    var PROVINCES = ["Agrigento", "Alessandria", "Ancona", "Aosta", "Arezzo", "Ascoli Piceno", "Asti", "Avellino", "Bari", "Barletta Andria Trani", "Belluno", "Benevento", "Bergamo", "Biella", "Bologna", "Bolzano", "Brescia", "Brindisi", "Cagliari", "Caltanissetta", "Campobasso", "Caserta", "Catania", "Catanzaro", "Chieti", "Como", "Cosenza", "Cremona", "Crotone", "Cuneo", "Enna", "Fermo", "Ferrara", "Firenze", "Foggia", "Forli Cesena", "Frosinone", "Genova", "Gorizia", "Grosseto", "Imperia", "Isernia", "L'Aquila", "La Spezia", "Latina", "Lecce", "Lecco", "Livorno", "Lodi", "Lucca", "Macerata", "Mantova", "Massa Carrara", "Matera", "Messina", "Milano", "Modena", "Monza Brianza", "Napoli", "Novara", "Nuoro", "Oristano", "Padova", "Palermo", "Parma", "Pavia", "Perugia", "Pesaro Urbino", "Pescara", "Piacenza", "Pisa", "Pistoia", "Pordenone", "Potenza", "Prato", "Ragusa", "Ravenna", "Reggio Calabria", "Reggio Emilia", "Rieti", "Rimini", "Roma", "Rovigo", "Salerno", "Sassari", "Savona", "Siena", "Siracusa", "Sondrio", "Taranto", "Teramo", "Terni", "Torino", "Trapani", "Trento", "Treviso", "Trieste", "Udine", "Varese", "Venezia", "Verbania", "Vercelli", "Verona", "Vibo Valentia", "Vicenza", "Viterbo"];

    var provSel = document.getElementById("province");
    var ph = document.createElement("option");
    ph.value = ""; ph.textContent = "Seleziona…";
    provSel.appendChild(ph);
    PROVINCES.forEach(function (p) {
        var o = document.createElement("option");
        o.value = p; o.textContent = p;
        provSel.appendChild(o);
    });

    var form = document.getElementById("reg-form");
    var btn = document.getElementById("submit-btn");
    var btnLabel = document.getElementById("btn-label");

    function errFor(el) {
        var n = el.parentElement;
        while (n) {
            var e = n.querySelector(".err");
            if (e) return e;
            n = n.parentElement;
        }
        return null;
    }

    function markField(id, on) {
        var el = document.getElementById(id);
        if (!el) return;
        el.classList.toggle("invalid", on);
        var err = errFor(el);
        if (err) err.classList.toggle("show", on);
    }

    function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }

    function validate() {
        var ok = true;
        [["name"], ["last_name"], ["company"], ["role"], ["province"]].forEach(function (f) {
            var el = document.getElementById(f[0]);
            var bad = !el.value.trim();
            markField(f[0], bad); if (bad) ok = false;
        });
        var email = document.getElementById("email");
        var badEmail = !validEmail(email.value.trim());
        markField("email", badEmail); if (badEmail) ok = false;

        var phone = document.getElementById("phone");
        var badPhone = phone.value.replace(/\D/g, "").length < 6;
        markField("phone", badPhone); if (badPhone) ok = false;

        var privacy = document.getElementById("privacy");
        var badPriv = !privacy.checked;
        var privErr = errFor(privacy);
        if (privErr) privErr.classList.toggle("show", badPriv);
        if (badPriv) ok = false;

        return ok;
    }

    function payload() {
        function cb(n) { var c = document.querySelector('input[name="' + n + '"]'); return c && c.checked ? "Sì" : "No"; }
        return {
            name: document.getElementById("name").value.trim(),
            last_name: document.getElementById("last_name").value.trim(),
            email: document.getElementById("email").value.trim(),
            prefix: document.getElementById("prefix").value,
            phone: document.getElementById("phone").value.trim(),
            company: document.getElementById("company").value.trim(),
            role: document.getElementById("role").value,
            province: document.getElementById("province").value,
            interest_webinar: cb("interest_webinar"),
            interest_kit: cb("interest_kit"),
            privacy: document.getElementById("privacy").checked ? "Sì" : "No",
            source: (window.UZTECH_CONFIG && window.UZTECH_CONFIG.SOURCE) || "Telesales"
        };
    }

    function setLoading(on) {
        btn.disabled = on;
        btn.style.opacity = on ? "0.7" : "";
        btnLabel.innerHTML = on ? '<span class="spin"></span>' : "Conferma iscrizione";
    }

    function onSuccess() {
        form.style.display = "none";
        document.getElementById("success").classList.remove("hidden");
        document.getElementById("iscriviti").scrollIntoView({ behavior: "smooth", block: "center" });
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!validate()) {
            var firstErr = form.querySelector(".invalid, .err.show");
            if (firstErr) firstErr.scrollIntoView({ behavior: "smooth", block: "center" });
            return;
        }
        var data = payload();
        var endpoint = window.UZTECH_CONFIG && window.UZTECH_CONFIG.ENDPOINT;

        if (!endpoint) {
            console.warn("UZTECH_CONFIG.ENDPOINT non configurato — invio simulato.", data);
            setLoading(true);
            setTimeout(function () { setLoading(false); onSuccess(); }, 700);
            return;
        }

        setLoading(true);
        // no-cors + text/plain: richiesta "semplice" senza preflight verso Apps Script.
        // La risposta è opaca: trattiamo la conclusione come successo.
        fetch(endpoint, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: JSON.stringify(data)
        }).then(function () { setLoading(false); onSuccess(); })
            .catch(function (err) {
                console.error(err);
                setLoading(false);
                alert("Si è verificato un problema durante l'invio. Riprova tra qualche istante.");
            });
    });

    form.addEventListener("input", function (e) {
        if (e.target.classList && e.target.classList.contains("field")) markField(e.target.id, false);
    });
    form.addEventListener("change", function (e) {
        var t = e.target;
        if (t.id === "privacy" && t.checked) {
            var err = errFor(t);
            if (err) err.classList.remove("show");
        }
    });
})();
