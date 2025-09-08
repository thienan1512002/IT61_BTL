document.addEventListener("DOMContentLoaded", function () {
  let performanceChart = null;
  let memoryChart = null;

  // Function to load rules data
  async function loadRulesData() {
    try {
      const response = await fetch("/Home/GetRules");
      const data = await response.json();
      updateRulesTables(data);
      updateCharts(data);
    } catch (error) {
      console.error("Error loading rules:", error);
    }
  }

  function updateCharts(data) {
    if (!data || !data.metadata) {
      console.error("Invalid data format received");
      return;
    }

    const aprioriMeta = data.metadata.apriori || {};
    const fpGrowthMeta = data.metadata.fpGrowth || {};

    // Update performance metrics on the page
    document.getElementById(
      "aprioriTime"
    ).textContent = `${aprioriMeta.execution_time}s`;
    document.getElementById(
      "aprioriMemory"
    ).textContent = `${aprioriMeta.memory_usage}MB`;
    document.getElementById(
      "aprioriCpu"
    ).textContent = `${aprioriMeta.cpu_usage}%`;
    document.getElementById("aprioriRulesCount").textContent =
      aprioriMeta.total_rules;

    document.getElementById(
      "fpTime"
    ).textContent = `${fpGrowthMeta.execution_time}s`;
    document.getElementById(
      "fpMemory"
    ).textContent = `${fpGrowthMeta.memory_usage}MB`;
    document.getElementById("fpCpu").textContent = `${fpGrowthMeta.cpu_usage}%`;
    document.getElementById("fpRulesCount").textContent =
      fpGrowthMeta.total_rules;

    // Performance Chart
    const perfCtx = document
      .getElementById("performanceChart")
      .getContext("2d");
    if (performanceChart) {
      performanceChart.destroy();
    }
    performanceChart = new Chart(perfCtx, {
      type: "bar",
      data: {
        labels: ["Processing Time (s)", "CPU Usage (%)", "Memory Usage (MB)"],
        datasets: [
          {
            label: "Apriori",
            data: [
              aprioriMeta.execution_time,
              aprioriMeta.cpu_usage,
              aprioriMeta.memory_usage,
            ],
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
          {
            label: "FP-Growth",
            data: [
              fpGrowthMeta.execution_time,
              fpGrowthMeta.cpu_usage,
              fpGrowthMeta.memory_usage,
            ],
            backgroundColor: "rgba(255, 99, 132, 0.5)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Algorithm Performance Comparison",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });

    // Memory Usage Chart
    const memCtx = document.getElementById("memoryChart").getContext("2d");
    if (memoryChart) {
      memoryChart.destroy();
    }
    memoryChart = new Chart(memCtx, {
      type: "pie",
      data: {
        labels: ["Apriori", "FP-Growth"],
        datasets: [
          {
            data: [aprioriMeta.memory_usage, fpGrowthMeta.memory_usage],
            backgroundColor: [
              "rgba(54, 162, 235, 0.5)",
              "rgba(255, 99, 132, 0.5)",
            ],
            borderColor: ["rgba(54, 162, 235, 1)", "rgba(255, 99, 132, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Memory Usage Comparison (MB)",
          },
        },
      },
    });
  }

  // Function to update rules tables
  function updateRulesTables(data) {
    if (!data || !data.aprioriRules || !data.fpGrowthRules) {
      console.error("Invalid rules data format");
      return;
    }

    const aprioriTable = document.getElementById("aprioriRules");
    const fpGrowthTable = document.getElementById("fpGrowthRules");

    if (!aprioriTable || !fpGrowthTable) {
      console.error("Tables not found in the DOM");
      return;
    }

    // Clear existing data
    aprioriTable.innerHTML = "";
    fpGrowthTable.innerHTML = "";

    // Update tables with new data
    data.aprioriRules.forEach((rule) => {
      aprioriTable.innerHTML += `
                <tr>
                    <td>${rule.antecedent || ""}</td>
                    <td>${rule.consequent || ""}</td>
                    <td>${rule.support.toFixed(3)}</td>
                    <td>${rule.confidence.toFixed(3)}</td>
                    <td>${rule.lift.toFixed(3)}</td>
                </tr>`;
    });

    data.fpGrowthRules.forEach((rule) => {
      fpGrowthTable.innerHTML += `
                <tr>
                    <td>${rule.antecedent || ""}</td>
                    <td>${rule.consequent || ""}</td>
                    <td>${rule.support.toFixed(3)}</td>
                    <td>${rule.confidence.toFixed(3)}</td>
                    <td>${rule.lift.toFixed(3)}</td>
                </tr>`;
    });
  }

  // Load initial data
  loadRulesData();
});
