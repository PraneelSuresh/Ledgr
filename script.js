window.openTransactionModal = () => {
  const modal = document.getElementById('transactionModal');
  const form = document.getElementById('transactionForm');
  
  if (modal) {
    if (form) {
      form.reset();
    }

    const idInput = document.getElementById('transactionId');
    if (idInput) {
      idInput.value = '';
    }

    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
      modalTitle.innerText = 'Add Transaction';
    }

    const dateInput = document.getElementById('transactionDate');
    if (dateInput) {
      if (!dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
      }
    }

    const typeSelect = document.getElementById('transactionType');
    if (typeSelect) {
      typeSelect.value = 'Expense';
    }

    window.toggleExpenseType();
    modal.classList.add('active');
  }
};

window.openEditTransactionModal = (button) => {
  const modal = document.getElementById('transactionModal');
  if (modal) {
    let rawType = button.dataset.type || 'Expense';
    let formattedType = rawType.charAt(0).toUpperCase() + rawType.slice(1).toLowerCase();

    const idInput = document.getElementById('transactionId');
    if (idInput) {
      idInput.value = button.dataset.id || '';
    }
    
    const typeSelect = document.getElementById('transactionType');
    if (typeSelect) {
      typeSelect.value = formattedType;
    }

    const amountInput = document.getElementById('transactionAmount');
    if (amountInput) {
      amountInput.value = button.dataset.amount || '';
    }

    const categoryInput = document.getElementById('transactionCategory');
    if (categoryInput) {
      categoryInput.value = button.dataset.category || '';
    }

    const expenseTypeInput = document.getElementById('transactionExpenseType');
    if (expenseTypeInput) {
      expenseTypeInput.value = button.dataset.expensetype || '';
    }

    const dateInput = document.getElementById('transactionDate');
    if (dateInput) {
      dateInput.value = button.dataset.date || '';
    }

    const descInput = document.getElementById('transactionDescription');
    if (descInput) {
      descInput.value = button.dataset.description || '';
    }

    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
      modalTitle.innerText = 'Edit Transaction';
    }

    window.toggleExpenseType();
    modal.classList.add('active');
  }
};

window.closeTransactionModal = () => {
  const modal = document.getElementById('transactionModal');
  if (modal) {
    modal.classList.remove('active');
  }
};

window.toggleExpenseType = () => {
  const typeSelect = document.getElementById("transactionType");
  const expenseTypeGroup = document.getElementById("expenseTypeGroup");
  const expenseTypeSelect = document.getElementById("transactionExpenseType");

  if (typeSelect && expenseTypeGroup) {
    let selectedValue = (typeSelect.value || '').toLowerCase();

    if (selectedValue === 'income') {
      expenseTypeGroup.style.display = "none";
      if (expenseTypeSelect) {
        expenseTypeSelect.value = "";
      }
    } else {
      expenseTypeGroup.style.display = "block";
      if (expenseTypeSelect && !expenseTypeSelect.value) {
        expenseTypeSelect.value = "Needs";
      }
    }
  }
};

if (typeof Chart !== 'undefined') {
  Chart.defaults.color = '#9ea4b0';
  Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
  Chart.defaults.scale.grid.color = '#2e333d';
}

const themeColors = {
  blue: '#3b82f6',
  blueHover: '#2563eb',
  red: '#ef4444',
  green: '#10b981',
  orange: '#f59e0b',
  purple: '#8b5cf6',
  surface: '#2c313a'
};

async function loadAnalyticsData() {
  try {
    const response = await fetch('/static/analytics.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    let categories = data.category_summary?.Category || [];
    let categoryAmounts = data.category_summary?.Amount || [];
    let expenseTypes = data.expense_type_summary?.["Expense Type"] || [];
    let expenseTotals = data.expense_type_summary?.["Expense Type Totals"] || [];

    const dashCanvas = document.getElementById('dashboardChart');
    if (dashCanvas) {
      new Chart(dashCanvas, {
        type: 'bar',
        data: {
          labels: categories.slice(0, 4),
          datasets: [{
            label: 'Spending',
            data: categoryAmounts.slice(0, 4),
            backgroundColor: themeColors.blue,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } }
        }
      });
    }

    const barCanvas = document.getElementById('barChart');
    if (barCanvas) {
      new Chart(barCanvas, {
        type: 'bar',
        indexAxis: 'y',
        data: {
          labels: categories,
          datasets: [{
            label: 'Amount',
            data: categoryAmounts,
            backgroundColor: themeColors.blueHover,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } }
        }
      });
    }

    const donutCanvas = document.getElementById('donutChart');
    if (donutCanvas) {
      new Chart(donutCanvas, {
        type: 'doughnut',
        data: {
          labels: expenseTypes,
          datasets: [{
            data: expenseTotals,
            backgroundColor: [themeColors.blue, themeColors.purple, themeColors.green, themeColors.orange],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '70%',
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    }

  } catch (error) {
    console.error("Error loading or rendering analytics data:", error);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('barChart') || document.getElementById('donutChart')) {
    loadAnalyticsData();
  }
});