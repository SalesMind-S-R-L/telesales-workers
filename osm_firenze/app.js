(function () {
    "use strict";

    var PROVINCES = ["Agrigento", "Alessandria", "Ancona", "Aosta", "Arezzo", "Ascoli Piceno", "Asti", "Avellino", "Bari", "Barletta Andria Trani", "Belluno", "Benevento", "Bergamo", "Biella", "Bologna", "Bolzano", "Brescia", "Brindisi", "Cagliari", "Caltanissetta", "Campobasso", "Carbonia Iglesias", "Caserta", "Catania", "Catanzaro", "Chieti", "Como", "Cosenza", "Cremona", "Crotone", "Cuneo", "Enna", "Fermo", "Ferrara", "Firenze", "Foggia", "Forli Cesena", "Frosinone", "Genova", "Gorizia", "Grosseto", "Imperia", "Isernia", "L'Aquila", "La Spezia", "Latina", "Lecce", "Lecco", "Livorno", "Lodi", "Lucca", "Macerata", "Mantova", "Massa Carrara", "Matera", "Medio Campidano", "Messina", "Milano", "Modena", "Monza Brianza", "Napoli", "Novara", "Nuoro", "Ogliastra", "Olbia", "Oristano", "Padova", "Palermo", "Parma", "Pavia", "Perugia", "Pesaro Urbino", "Pescara", "Piacenza", "Pisa", "Pistoia", "Pordenone", "Potenza", "Prato", "Ragusa", "Ravenna", "Reggio Calabria", "Reggio Emilia", "Rieti", "Rimini", "Roma", "Rovigo", "Salerno", "San Marino", "Sassari", "Savona", "Siena", "Siracusa", "Sondrio", "Taranto", "Teramo", "Terni", "Torino", "Trapani", "Trento", "Treviso", "Trieste", "Udine", "Varese", "Venezia", "Verbania", "Vercelli", "Verona", "Vibo Valentia", "Vicenza", "Viterbo"];

    // popola dropdown province (Firenze preselezionata)
    var provSel = document.getElementById("province");
    PROVINCES.forEach(function (p) {
        var o = document.createElement("option");
        o.value = p; o.textContent = p;
        if (p === "Firenze") o.selected = true;
        provSel.appendChild(o);
    });

    var form = document.getElementById("reg-form");
    var btn = document.getElementById("submit-btn");
    var btnLabel = document.getElementById("btn-label");

    // risale gli antenati finché non trova il messaggio di errore associato al campo
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

    function markGroup(name, on) {
        var el = document.querySelector('input[name="' + name + '"]');
        if (!el) return;
        var err = errFor(el);
        if (err) err.classList.toggle("show", on);
    }

    function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }

    function validate() {
        var ok = true;
        [["name"], ["last_name"], ["city"], ["company"], ["province"], ["role"]].forEach(function (f) {
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

        ["consent31", "consent32"].forEach(function (n) {
            var bad = !document.querySelector('input[name="' + n + '"]:checked');
            markGroup(n, bad); if (bad) ok = false;
        });
        return ok;
    }

    function payload() {
        function rb(n) { var c = document.querySelector('input[name="' + n + '"]:checked'); return c ? c.value : ""; }
        return {
            name: document.getElementById("name").value.trim(),
            last_name: document.getElementById("last_name").value.trim(),
            email: document.getElementById("email").value.trim(),
            prefix: document.getElementById("prefix").value,
            phone: document.getElementById("phone").value.trim(),
            city: document.getElementById("city").value.trim(),
            company: document.getElementById("company").value.trim(),
            role: document.getElementById("role").value,
            province: document.getElementById("province").value,
            privacy: document.getElementById("privacy").checked ? "Sì" : "No",
            consent31: rb("consent31"),
            consent32: rb("consent32"),
            source: (window.OSM_CONFIG && window.OSM_CONFIG.SOURCE) || "Telesales"
        };
    }

    function setLoading(on) {
        btn.disabled = on;
        btn.style.opacity = on ? "0.7" : "";
        btnLabel.innerHTML = on ? '<span class="spin"></span>' : "Conferma iscrizione";
        btnLabel.parentElement.classList.toggle("pointer-events-none", on);
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
        var endpoint = window.OSM_CONFIG && window.OSM_CONFIG.ENDPOINT;

        if (!endpoint) {
            // modalità DEMO: nessun endpoint configurato
            console.warn("OSM_CONFIG.ENDPOINT non configurato — invio simulato.", data);
            setLoading(true);
            setTimeout(function () { setLoading(false); onSuccess(); }, 700);
            return;
        }

        setLoading(true);
        // no-cors + text/plain: richiesta "semplice" senza preflight verso Apps Script.
        // La risposta è opaca (non leggibile), ma la riga viene scritta: trattiamo la
        // conclusione come successo.
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

    // pulizia errori al volo
    form.addEventListener("input", function (e) {
        if (e.target.classList && e.target.classList.contains("field")) markField(e.target.id, false);
    });
    form.addEventListener("change", function (e) {
        var t = e.target;
        if (t.type === "checkbox" || t.type === "radio") {
            var err = errFor(t);
            if (err) err.classList.remove("show");
        }
    });
})();
