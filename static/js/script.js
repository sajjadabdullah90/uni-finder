
const searchForm = document.getElementById("searchForm");
const universityNameInput = document.getElementById("universityName");
const countryInput = document.getElementById("country");
const searchButton = document.getElementById("searchButton");
const resultsContainer = document.getElementById("results");
const resultCount = document.getElementById("resultCount");

function showMessage(title, description, type = "empty") {
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
    paragraph.textContent = "Connecting to the live university database.";

    state.append(spinner, heading, paragraph);
    resultsContainer.appendChild(state);

    resultCount.textContent = "SEARCHING...";
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

    const websites = Array.isArray(university.web_pages)
        ? university.web_pages
        : [];

    card.append(top, name, domain);

    if (websites.length) {
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

            const label = document.createElement("span");
            label.textContent = "Visit official website";

            const arrow = document.createElement("span");
            arrow.textContent = "↗";

            link.append(label, arrow);
            card.appendChild(link);
        }
    }

    return card;
}

function displayResults(universities) {
    resultsContainer.replaceChildren();

    if (!universities.length) {
        showMessage(
            "No universities found.",
            "Try another university name or country."
        );

        resultCount.textContent = "0 RESULTS";
        return;
    }

    const fragment = document.createDocumentFragment();

    universities.forEach((university, index) => {
        fragment.appendChild(
            createUniversityCard(university, index)
        );
    });

    resultsContainer.appendChild(fragment);
    resultCount.textContent =
        `${universities.length.toLocaleString()} RESULTS`;

    document.getElementById("resultsSection").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function searchUniversities(name, country) {
    const params = new URLSearchParams();

    if (name) params.set("name", name);
    if (country) params.set("country", country);

    searchButton.disabled = true;
    searchButton.querySelector("span:first-child").textContent = "Searching...";

    showLoading();

    try {
        const response = await fetch(
            `/api/universities?${params.toString()}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        displayResults(data.results || []);

    } catch (error) {
        console.error("Search error:", error);

        showMessage(
            "Something went wrong.",
            error.message || "Unable to connect to the university database.",
            "error"
        );

        resultCount.textContent = "ERROR";

    } finally {
        searchButton.disabled = false;
        searchButton.querySelector("span:first-child").textContent =
            "Search universities";
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
        resultCount.textContent = "0 RESULTS";
        return;
    }

    searchUniversities(name, country);
});

document.querySelectorAll(".quick-chip").forEach(button => {
    button.addEventListener("click", () => {
        countryInput.value = button.dataset.country;
        universityNameInput.value = "";

        searchUniversities("", button.dataset.country);
    });
});
