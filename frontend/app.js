
const apiStatus = document.querySelector("#api-status");
const apiMetric = document.querySelector("#api-metric");
const statusDot = document.querySelector(".status-dot");

const incidentList = document.querySelector("#incident-list");
const totalIncidents = document.querySelector("#total-incidents");
const criticalCount = document.querySelector("#critical-count");
const highCount = document.querySelector("#high-count");

const refreshButton = document.querySelector("#refresh-button");
const openFormButton = document.querySelector("#open-form-button");
const closeFormButton = document.querySelector("#close-form-button");
const reportSection = document.querySelector("#report-section");
const incidentForm = document.querySelector("#incident-form");
const formFeedback = document.querySelector("#form-feedback");
const submitButton = document.querySelector("#submit-button");

const detailSection = document.querySelector("#detail-section");
const incidentDetail = document.querySelector("#incident-detail");
const closeDetailButton = document.querySelector("#close-detail-button");
const modalBackdrop = document.querySelector("#modal-backdrop");

let incidentsExpanded = false;
let loadedIncidents = [];

// -----------------------------
// API connection status
// -----------------------------

function updateApiStatus(isOnline) {
    apiStatus.textContent = isOnline ? "Connected" : "Unavailable";
    apiMetric.textContent = isOnline ? "Online" : "Offline";

    apiMetric.className = isOnline
        ? "status-online"
        : "status-offline";

    statusDot.classList.toggle("online", isOnline);
    statusDot.classList.toggle("offline", !isOnline);
}

// -----------------------------
// Load incidents
// -----------------------------

async function loadIncidents() {
    incidentList.replaceChildren();

    const loadingMessage = document.createElement("p");
    loadingMessage.textContent = "Loading incidents...";
    incidentList.appendChild(loadingMessage);

    try {
        const response = await fetch("/incidents?limit=100&skip=0");

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const incidents = await response.json();

        updateApiStatus(true);
        updateMetrics(incidents);
        renderIncidents(incidents);
    } catch (error) {
        updateApiStatus(false);
        incidentList.replaceChildren();

        const errorMessage = document.createElement("p");
        errorMessage.textContent =
            "Could not load incidents. Check the API connection.";
        incidentList.appendChild(errorMessage);

        console.error("Error loading incidents:", error);
    }
}

// -----------------------------
// Dashboard metrics
// -----------------------------

function updateMetrics(incidents) {
    totalIncidents.textContent = incidents.length;

    criticalCount.textContent = incidents.filter(
        (incident) => incident.analysis?.severity === "critical"
    ).length;

    highCount.textContent = incidents.filter(
        (incident) => incident.analysis?.severity === "high"
    ).length;
}

// -----------------------------
// Render incident list
// -----------------------------

function renderIncidents(incidents) {
    incidentList.replaceChildren();
    loadedIncidents = incidents;

    if (incidents.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No incidents recorded yet.";
        incidentList.appendChild(emptyMessage);
        return;
    }

    const visibleIncidents = incidentsExpanded
        ? incidents
        : incidents.slice(0, 3);

    visibleIncidents.forEach((incident) => {
        const item = document.createElement("article");
        item.className = "incident-item";
        item.tabIndex = 0;
        item.setAttribute("role", "button");
        item.setAttribute(
            "aria-label",
            `View incident details for ${incident.service || "unknown service"}`
        );

        item.addEventListener("click", () => {
            showIncidentDetails(incident._id);
        });

        item.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                showIncidentDetails(incident._id);
            }
        });

        const info = document.createElement("div");
        info.className = "incident-info";

        const service = document.createElement("h3");
        service.textContent = incident.service || "Unknown service";

        const message = document.createElement("p");
        message.textContent = incident.message || "No message";

        const metadata = document.createElement("p");
        metadata.textContent =
            `${incident.environment || "unknown"} · ` +
            `${incident.level || "unknown"} · ` +
            `${formatDate(incident.timestamp)}`;

        const severity = document.createElement("span");
        const severityValue =
            incident.analysis?.severity || "unknown";

        severity.className =
            `severity-badge severity-${severityValue}`;
        severity.textContent = severityValue.toUpperCase();

        info.append(service, message, metadata);
        item.append(info, severity);
        incidentList.appendChild(item);
    });

    if (incidents.length > 3) {
        const toggleButton = document.createElement("button");

        toggleButton.type = "button";
        toggleButton.className = "view-more-button";
        toggleButton.textContent = incidentsExpanded
            ? "Ver menos"
            : `Ver más (${incidents.length - 3})`;

        toggleButton.addEventListener("click", () => {
            incidentsExpanded = !incidentsExpanded;
            renderIncidents(loadedIncidents);
        });

        incidentList.appendChild(toggleButton);
    }
}

function formatDate(timestamp) {
    if (!timestamp) {
        return "Date unavailable";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        return String(timestamp);
    }

    return date.toLocaleString();
}

// -----------------------------
// Open and close report form
// -----------------------------

openFormButton.addEventListener("click", () => {
    reportSection.hidden = false;
    reportSection.classList.remove("hidden");

    reportSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
});

closeFormButton.addEventListener("click", () => {
    reportSection.hidden = true;
    reportSection.classList.add("hidden");
    formFeedback.textContent = "";
});

// -----------------------------
// Submit new incident
// -----------------------------


incidentForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    formFeedback.textContent = "";
    submitButton.disabled = true;
    submitButton.textContent = "Analyzing...";

    
    const incidentData = {
        service: incidentForm.elements["service"].value.trim(),
        environment: incidentForm.elements["environment"].value,
        level: incidentForm.elements["level"].value,
        message: incidentForm.elements["message"].value.trim(),
        timestamp: new Date().toISOString(),
    };


    let incidentCreated = false;

    try {
        const response = await fetch("/incidents", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(incidentData),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(
                `Request failed (${response.status}): ${errorText}`
            );
        }

        const result = await response.json();

        formFeedback.textContent =
            `Incident reported successfully! Severity: ` +
            `${result.analysis.severity.toUpperCase()}`;

        incidentForm.reset();
        incidentsExpanded = false;
        incidentCreated = true;

    } catch (error) {
        formFeedback.textContent =
            "Could not report incident. Please try again.";

        console.error("Error reporting incident:", error);

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Submit incident";
    }

    // Refresh the dashboard after restoring the button.
    if (incidentCreated) {
        loadIncidents();
    }
});


// -----------------------------
// Refresh list
// -----------------------------

refreshButton.addEventListener("click", loadIncidents);

// Initial load
loadIncidents();


async function showIncidentDetails(incidentId) {
    detailSection.hidden = false;
    incidentDetail.replaceChildren();

    const loading = document.createElement("p");
    loading.textContent = "Loading incident details...";
    incidentDetail.appendChild(loading);

    try {
        const response = await fetch(
            `/incidents/${encodeURIComponent(incidentId)}`
        );

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const incident = await response.json();
        renderIncidentDetails(incident);
    } catch (error) {
        console.error("Error loading incident details:", error);
        incidentDetail.replaceChildren();

        const message = document.createElement("p");
        message.textContent =
            "Could not load incident details. Please try again.";
        incidentDetail.appendChild(message);
    }
}

function renderIncidentDetails(incident) {
    incidentDetail.replaceChildren();

    const analysis = incident.analysis || {};

    addDetailSection(
        incidentDetail,
        "Error message",
        incident.message || "No message available"
    );

    const metadata = document.createElement("div");
    metadata.className = "detail-meta";

    [
        `Service: ${incident.service || "Unknown"}`,
        `Environment: ${incident.environment || "Unknown"}`,
        `Level: ${incident.level || "Unknown"}`,
        `Severity: ${(analysis.severity || "unknown").toUpperCase()}`
    ].forEach((value) => {
        const tag = document.createElement("span");
        tag.className = "detail-tag";
        tag.textContent = value;
        metadata.appendChild(tag);
    });

    incidentDetail.appendChild(metadata);

    addDetailList(
        incidentDetail,
        "Probable causes",
        analysis.probable_causes
    );

    addDetailList(
        incidentDetail,
        "Recommended actions",
        analysis.recommended_actions
    );

    addDetailList(
        incidentDetail,
        "Matched rules",
        analysis.matched_rules
    );

    addDetailList(
        incidentDetail,
        "Categories",
        analysis.categories
    );
}

function addDetailSection(container, heading, content) {
    const section = document.createElement("div");
    section.className = "detail-section";

    const title = document.createElement("h3");
    title.textContent = heading;

    const text = document.createElement("p");
    text.textContent = content;

    section.append(title, text);
    container.appendChild(section);
}

function addDetailList(container, heading, items) {
    const section = document.createElement("div");
    section.className = "detail-section";

    const title = document.createElement("h3");
    title.textContent = heading;
    section.appendChild(title);

    const list = document.createElement("ul");

    if (Array.isArray(items) && items.length > 0) {
        items.forEach((item) => {
            const listItem = document.createElement("li");
            listItem.textContent = item;
            list.appendChild(listItem);
        });
    } else {
        const listItem = document.createElement("li");
        listItem.textContent = "No information available";
        list.appendChild(listItem);
    }

    section.appendChild(list);
    container.appendChild(section);
}

function closeIncidentDetails() {
    detailSection.hidden = true;
}

closeDetailButton.addEventListener("click", closeIncidentDetails);
modalBackdrop.addEventListener("click", closeIncidentDetails);

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !detailSection.hidden) {
        closeIncidentDetails();
    }
});

