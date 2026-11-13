
const searchForm = document.getElementById("searchForm");
const universityNameInput = document.getElementById("universityName");
const countryInput = document.getElementById("country");
const searchButton = document.getElementById("searchButton");
const clearButton = document.getElementById("clearButton");
const resultsContainer = document.getElementById("results");
const resultCount = document.getElementById("resultCount");

let activeController = null;
let lastSearch = { name: "", country: "" };

function updateResultCount(value) {
    resultCount.textContent = value;
}

function showMessage(title, description, type = "empty", retry = false) {
    resultsContainer.replaceChildren();

    const state = document.createElement("div");
    state.className = "empty-state";

    const icon = document.createElement("div");
    icon.className = "empty-icon";
    icon.textContent = type === "error" ? "!" : "⌕";

    const heading = document.createElement("h3");
    heading.textContent = title;

    const paragraph = document.createElement("p");
    paragraph.textContent = description;

    if (type === "error") {
        paragraph.classList.add("error-text");
    }

    state.append(icon, heading, paragraph);

    if (retry) {
        const retryButton = document.createElement("button");
        retryButton.type = "button";
        retryButton.className = "quick-chip";
        retryButton.textContent = "Try again";

        retryButton.addEventListener("click", () => {
            searchUniversities(lastSearch.name, lastSearch.country);
        });

        state.appendChild(retryButton);
    }

    resultsContainer.appendChild(state);
}

function showLoading() {
    resultsContainer.replaceChildren();

    const state = document.createElement("div");
    state.className = "empty-state";

    const spinner = document.createElement("div");
    spinner.className = "loading-spinner";

    const heading = document.createElement("h3");
    heading.textContent = "Searching universities...";

    const paragraph = document.createElement("p");
    paragraph.textContent = "Connecting to the university database.";

    state.append(spinner, heading, paragraph);
    resultsContainer.appendChild(state);

    resultsContainer.setAttribute("aria-busy", "true");
    updateResultCount("SEARCHING...");
}

function setSearching(isSearching) {
    searchButton.disabled = isSearching;
    searchButton.querySelector("span:first-child").textContent =
        isSearching ? "Searching..." : "Search universities";

    resultsContainer.setAttribute("aria-busy", String(isSearching));
}

function getInitials(name) {
    return name
        .split(/\s+/)
        .filter(Boolean)
        .slice(0, 2)
        .map(word => word[0].toUpperCase())
        .join("");
}

function createUniversityCard(university, index) {
    const card = document.createElement("article");
    card.className = "university-card";
    card.style.animationDelay = `${Math.min(index * 45, 450)}ms`;

    const top = document.createElement("div");
    top.className = "card-top";

    const avatar = document.createElement("div");
    avatar.className = "university-avatar";
    avatar.textContent = getInitials(university.name || "University");

    const countryTag = document.createElement("span");
    countryTag.className = "country-tag";
    countryTag.textContent = university.country || "Unknown country";

    top.append(avatar, countryTag);

    const name = document.createElement("h3");
    name.textContent = university.name || "Unnamed university";

    const domain = document.createElement("p");

    const domains = Array.isArray(university.domains)
        ? university.domains
        : [];

    domain.textContent = domains.length
        ? domains.join(", ")
        : "Official website information unavailable";

    card.append(top, name, domain);

    const websites = Array.isArray(university.web_pages)
        ? university.web_pages
        : [];

    const website = websites.find(url => {
        try {
            const parsed = new URL(url);
            return ["http:", "https:"].includes(parsed.protocol);
        } catch {
            return false;
        }
    });

    if (website) {
        const link = document.createElement("a");

        link.className = "visit-link";
        link.href = website;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.setAttribute("aria-label", `Visit official website of ${name.textContent}`);

        const label = document.createElement("span");
        label.textContent = "Visit official website";

        const arrow = document.createElement("span");
        arrow.textContent = "↗";
        arrow.setAttribute("aria-hidden", "true");

        link.append(label, arrow);
        card.appendChild(link);
    }

    return card;
}

function displayResults(universities) {
    resultsContainer.replaceChildren();

    if (!Array.isArray(universities) || universities.length === 0) {
        showMessage(
            "No universities found.",
            "Try another university name or country. You can also check your spelling."
        );

        updateResultCount("0 RESULTS");
        return;
    }

    const fragment = document.createDocumentFragment();

    universities.forEach((university, index) => {
        fragment.appendChild(
            createUniversityCard(university, index)
        );
    });

    resultsContainer.appendChild(fragment);

    updateResultCount(
        `${universities.length.toLocaleString()} RESULTS`
    );

    document.getElementById("resultsSection").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function searchUniversities(name, country) {
    lastSearch = { name, country };

    if (activeController) {
        activeController.abort();
    }

    const controller = new AbortController();
    activeController = controller;

    const params = new URLSearchParams();

    if (name) params.set("name", name);
    if (country) params.set("country", country);

    setSearching(true);
    showLoading();

    try {
        const response = await fetch(
            `/api/universities?${params.toString()}`,
            { signal: controller.signal }
        );

        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error("The server returned an invalid response.");
        }

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to retrieve university information."
            );
        }

        if (!Array.isArray(data.results)) {
            throw new Error("Unexpected data received from the university database.");
        }

        displayResults(data.results);

    } catch (error) {
        if (error.name === "AbortError") {
            return;
        }

        console.error("Search error:", error);

        showMessage(
            "Unable to complete your search.",
            error.message || "Please check your connection and try again.",
            "error",
            true
        );

        updateResultCount("ERROR");

    } finally {
        if (activeController === controller) {
            activeController = null;
            setSearching(false);
        }
    }
}

searchForm.addEventListener("submit", event => {
    event.preventDefault();

    const name = universityNameInput.value.trim();
    const country = countryInput.value.trim();

    if (!name && !country) {
        showMessage(
            "Let's start exploring.",
            "Enter a university name or country to begin."
        );

        updateResultCount("0 RESULTS");
        universityNameInput.focus();
        return;
    }

    searchUniversities(name, country);
});

document.querySelectorAll(".quick-chip[data-country]").forEach(button => {
    button.addEventListener("click", () => {
        const country = button.dataset.country;

        universityNameInput.value = "";
        countryInput.value = country;

        searchUniversities("", country);
    });
});

clearButton.addEventListener("click", () => {
    if (activeController) {
        activeController.abort();
        activeController = null;
    }

    universityNameInput.value = "";
    countryInput.value = "";

    setSearching(false);

    showMessage(
        "Your next destination awaits.",
        "Enter a university name or country above to discover universities."
    );

    updateResultCount("0 RESULTS");

    universityNameInput.focus();
});

