// Base URL handling
window.getBaseUrl = () => {
  const isGitHubPages = window.location.hostname.includes("github.io");
  return isGitHubPages ? "/HelloWorldGitHub/" : "/";
};

// Update href attributes with base URL
function updateLinks() {
  document.querySelectorAll("[data-href]").forEach((element) => {
    const path = element.getAttribute("data-href");
    element.href = window.getBaseUrl() + path;
  });
}

async function loadComponent(id, path) {
  try {
    const baseUrl = getBaseUrl();
    const response = await fetch(baseUrl + path);
    const html = await response.text();
    document.getElementById(id).innerHTML = html;
  } catch (error) {
    console.error(`Error loading ${path}:`, error);
  }
}

function populateCompoundData(data) {
  // Update page title and navigation
  document.title = `${data.name} - PED Knowledge Base`;
  document.getElementById("compound-name").textContent = data.name;
  document.getElementById("compound-title").textContent = data.name;
  document.getElementById("compound-category").textContent = data.category;

  // Populate quick navigation
  const quickNav = document.getElementById("quick-nav");
  quickNav.innerHTML = data.quickNavigation
    .map(
      (item) => `
    <li>
      <a href="#${item.id}" class="text-gray-600 hover:text-gray-900">${item.title}</a>
    </li>
  `
    )
    .join("");

  // Populate overview section
  document.getElementById("chemical-name").textContent =
    data.overview.chemicalName;
  document.getElementById("half-life").innerHTML = Object.entries(
    data.overview.halfLife
  )
    .map(([type, time]) => `${type}: ${time}`)
    .join("<br>");
  document.getElementById("detection-time").textContent =
    data.overview.detectionTime;

  // Populate dosage calculator
  const experienceLevel = document.getElementById("experience-level");
  experienceLevel.innerHTML = data.dosageGuidelines.calculator.experienceLevels
    .map((level) => `<option>${level}</option>`)
    .join("");

  const trainingGoal = document.getElementById("training-goal");
  trainingGoal.innerHTML = data.dosageGuidelines.calculator.goals
    .map((goal) => `<option>${goal}</option>`)
    .join("");

  // Update dosage recommendation based on selection
  function updateDosageRecommendation() {
    const level = experienceLevel.value.toLowerCase();
    document.getElementById("dosage-recommendation").textContent =
      data.dosageGuidelines.calculator.recommendations[level];
  }

  experienceLevel.addEventListener("change", updateDosageRecommendation);
  trainingGoal.addEventListener("change", updateDosageRecommendation);
  updateDosageRecommendation(); // Initial update

  // Populate effects
  document.getElementById("effects-list").innerHTML = data.effects.benefits
    .map(
      (effect) => `
    <div class="flex items-start">
      <div class="flex-shrink-0">
        <i class="fas fa-check text-green-500"></i>
      </div>
      <div class="ml-3">
        <h3 class="text-lg font-medium text-gray-900">${effect.title}</h3>
        <p class="mt-1 text-gray-500">${effect.description}</p>
      </div>
    </div>
  `
    )
    .join("");

  // Populate side effects
  document.getElementById("side-effects-warning").textContent =
    data.sideEffects.warning;
  document.getElementById("side-effects-list").innerHTML =
    data.sideEffects.categories
      .map(
        (effect) => `
    <div class="flex items-start">
      <div class="flex-shrink-0">
        <i class="fas fa-exclamation-circle text-red-500"></i>
      </div>
      <div class="ml-3">
        <h3 class="text-lg font-medium text-gray-900">${effect.type}</h3>
        <p class="mt-1 text-gray-500">${effect.description}</p>
      </div>
    </div>
  `
      )
      .join("");

  // Populate PCT requirements
  document.getElementById("pct-content").innerHTML = `
    <p class="text-gray-500">Standard PCT protocol following cycle:</p>
    <ul class="mt-4 space-y-2 text-gray-500">
      ${data.pct.protocol.map((step) => `<li>${step}</li>`).join("")}
    </ul>
  `;

  // Populate studies
  document.getElementById("studies-list").innerHTML = data.studies
    .map(
      (study) => `
    <div class="border-l-4 border-blue-500 pl-4">
      <h3 class="text-lg font-medium text-gray-900">${study.title}</h3>
      <p class="mt-2 text-gray-500">${study.description}</p>
      <p class="mt-2 text-sm text-gray-400">${study.source}</p>
    </div>
  `
    )
    .join("");
}

// Initialize page
document.addEventListener("DOMContentLoaded", async () => {
  // Import compound data
  const { compoundData } = await import("../data/compound-data.js");

  // Load all components
  await Promise.all([
    loadComponent("navigation", "/components/navigation.html"),
    loadComponent("footer", "/components/footer.html"),
  ]);

  // Populate data
  populateCompoundData(compoundData);
  updateLinks();
});
