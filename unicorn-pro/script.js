// ============================================
// UNICORN PRO — DASHBOARD CHARTS & INTERACTIONS
// ============================================

// --- Chart.js Global Defaults ---
Chart.defaults.color = '#9898b0';
Chart.defaults.borderColor = '#2a2a3a';
Chart.defaults.font.family = "'Inter', sans-serif";

const PURPLE = 'rgba(124, 58, 237, 0.85)';
const PURPLE_DIM = 'rgba(124, 58, 237, 0.3)';
const GREEN = 'rgba(34, 197, 94, 0.85)';
const RED = 'rgba(239, 68, 68, 0.85)';
const YELLOW = 'rgba(245, 158, 11, 0.85)';
const BLUE = 'rgba(59, 130, 246, 0.85)';
const ORANGE = 'rgba(249, 115, 22, 0.85)';

// === DATA (computed from raw CSV) ===
const DATA = {
  verticals: {
    roofing:  { leads: 2409, cost: 59102.76, revenue: 75962.81, profit: 16860.05, sold: 1976, returned: 248, unsold: 185 },
    bathroom: { leads: 1361, cost: 38351.93, revenue: 45923.30, profit: 7571.37,  sold: 1081, returned: 130, unsold: 150 },
    windows:  { leads: 1553, cost: 33166.53, revenue: 36370.56, profit: 3204.03,  sold: 1248, returned: 180, unsold: 125 }
  },
  sources: {
    facebook: { leads: 3331, cost: 76925.52, revenue: 98384.54, profit: 21459.02 },
    native:   { leads: 648,  cost: 12271.25, revenue: 19796.51, profit: 7525.26  },
    google:   { leads: 1344, cost: 41424.45, revenue: 40075.62, profit: -1348.83 }
  },
  buyers: {
    BuyerA: { leads: 1528, cost: 35388.17, revenue: 46387.99, profit: 10999.82 },
    BuyerB: { leads: 1468, cost: 36443.97, revenue: 47180.90, profit: 10736.93 },
    BuyerC: { leads: 443,  cost: 10935.35, revenue: 20475.79, profit: 9540.44  },
    BuyerD: { leads: 816,  cost: 20174.44, revenue: 24210.61, profit: 4036.17  },
    BuyerE: { leads: 476,  cost: 13388.07, revenue: 16789.51, profit: 3401.44  },
    BuyerF: { leads: 132,  cost: 2787.63,  revenue: 3211.87,  profit: 424.24   }
  },
  days: {
    Monday:    { profit: 5521.81, cost: 23437.50, revenue: 28959.31, leads: 958 },
    Tuesday:   { profit: 5592.96, cost: 23910.42, revenue: 29503.38, leads: 981 },
    Wednesday: { profit: 3752.59, cost: 18412.53, revenue: 22165.12, leads: 739 },
    Thursday:  { profit: 4183.58, cost: 19608.43, revenue: 23792.01, leads: 805 },
    Friday:    { profit: 4283.01, cost: 17962.71, revenue: 22245.72, leads: 732 },
    Saturday:  { profit: 1726.47, cost: 13598.01, revenue: 15324.48, leads: 551 },
    Sunday:    { profit: 2575.03, cost: 13691.62, revenue: 16266.65, leads: 557 }
  },
  returnReasons: {
    'no_answer':           { count: 186, cost_lost: 4574.52 },
    'bad_number':          { count: 113, cost_lost: 2716.93 },
    'not_homeowner':       { count: 85,  cost_lost: 1977.97 },
    'out_of_service_area': { count: 61,  cost_lost: 1470.68 },
    'changed_mind':        { count: 59,  cost_lost: 1411.05 },
    'duplicate':           { count: 54,  cost_lost: 1366.60 }
  },
  states: {
    TX: { leads: 656, profit: 5869.49, cost: 16145.62, unsold: 45 },
    FL: { leads: 539, profit: 5130.62, cost: 13352.98, unsold: 37 },
    GA: { leads: 409, profit: 3677.31, cost: 10065.51, unsold: 32 },
    CA: { leads: 466, profit: 1870.33, cost: 11536.51, unsold: 29 },
    PA: { leads: 261, profit: 1295.76, cost: 6461.66,  unsold: 10 },
    TN: { leads: 211, profit: 1246.04, cost: 5213.46,  unsold: 5  },
    NY: { leads: 215, profit: 1168.87, cost: 5302.38,  unsold: 14 },
    MI: { leads: 218, profit: 1111.90, cost: 5188.45,  unsold: 14 },
    OH: { leads: 310, profit: 1140.45, cost: 7577.24,  unsold: 32 },
    NC: { leads: 334, profit: 1110.86, cost: 7996.72,  unsold: 28 },
    IL: { leads: 230, profit: 923.04,  cost: 5590.10,  unsold: 19 },
    SC: { leads: 170, profit: 715.98,  cost: 4134.24,  unsold: 17 },
    CO: { leads: 171, profit: 788.97,  cost: 4202.14,  unsold: 13 },
    AZ: { leads: 257, profit: 807.39,  cost: 6299.02,  unsold: 26 },
    NJ: { leads: 145, profit: 554.83,  cost: 3465.00,  unsold: 11 },
    MO: { leads: 159, profit: 572.01,  cost: 4013.76,  unsold: 12 },
    IN: { leads: 126, profit: 619.49,  cost: 3034.14,  unsold: 8  },
    VA: { leads: 166, profit: 653.07,  cost: 4126.75,  unsold: 12 },
    WY: { leads: 64,  profit: -119.91, cost: 1587.96,  unsold: 19 },
    ID: { leads: 88,  profit: -499.00, cost: 2113.98,  unsold: 30 },
    MT: { leads: 78,  profit: -712.95, cost: 1959.85,  unsold: 29 },
    ND: { leads: 50,  profit: -289.10, cost: 1253.75,  unsold: 18 }
  }
};

// === CHART 1: Source Profit ===
function drawSourceChart() {
  const ctx = document.getElementById('sourceChart');
  if (!ctx) return;

  const labels = Object.keys(DATA.sources);
  const profits = labels.map(k => DATA.sources[k].profit);
  const roi = labels.map(k => {
    const d = DATA.sources[k];
    return parseFloat(((d.profit / d.cost) * 100).toFixed(1));
  });
  const colors = profits.map(p => p < 0 ? RED : p > 7000 ? GREEN : PURPLE);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
      datasets: [
        {
          label: 'Прибуток ($)',
          data: profits,
          backgroundColor: colors,
          borderRadius: 8,
          borderSkipped: false,
          yAxisID: 'y'
        },
        {
          label: 'ROI (%)',
          data: roi,
          type: 'line',
          borderColor: YELLOW,
          backgroundColor: 'transparent',
          borderWidth: 2,
          pointBackgroundColor: YELLOW,
          pointRadius: 5,
          yAxisID: 'y1',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { position: 'bottom', labels: { usePointStyle: true, padding: 16 } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              if (ctx.dataset.label === 'ROI (%)') return ` ROI: ${ctx.raw}%`;
              return ` Прибуток: $${ctx.raw.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        y: {
          type: 'linear',
          position: 'left',
          grid: { color: '#2a2a3a' },
          ticks: { callback: v => `$${(v/1000).toFixed(0)}K` }
        },
        y1: {
          type: 'linear',
          position: 'right',
          grid: { display: false },
          ticks: { callback: v => `${v}%` }
        }
      }
    }
  });
}

// === CHART 2: Vertical Performance ===
function drawVerticalChart() {
  const ctx = document.getElementById('verticalChart');
  if (!ctx) return;

  const labels = ['Roofing', 'Bathroom', 'Windows'];
  const data = [DATA.verticals.roofing, DATA.verticals.bathroom, DATA.verticals.windows];

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Дохід',
          data: data.map(d => d.revenue),
          backgroundColor: 'rgba(124,58,237,0.6)',
          borderRadius: 6,
          borderSkipped: false,
        },
        {
          label: 'Витрати',
          data: data.map(d => d.cost),
          backgroundColor: 'rgba(239,68,68,0.5)',
          borderRadius: 6,
          borderSkipped: false,
        },
        {
          label: 'Прибуток',
          data: data.map(d => d.profit),
          backgroundColor: data.map(d => d.profit > 0 ? 'rgba(34,197,94,0.8)' : RED),
          borderRadius: 6,
          borderSkipped: false,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { usePointStyle: true, padding: 16 } },
        tooltip: { callbacks: { label: (ctx) => ` ${ctx.dataset.label}: $${ctx.raw.toLocaleString()}` } }
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: '#2a2a3a' }, ticks: { callback: v => `$${(v/1000).toFixed(0)}K` } }
      }
    }
  });
}

// === CHART 3: Day of Week ROI ===
function drawDayChart() {
  const ctx = document.getElementById('dayChart');
  if (!ctx) return;

  const days = Object.keys(DATA.days);
  const roi = days.map(d => parseFloat(((DATA.days[d].profit / DATA.days[d].cost) * 100).toFixed(1)));
  const profit = days.map(d => DATA.days[d].profit);
  const colors = roi.map(r => r < 15 ? 'rgba(245,158,11,0.7)' : 'rgba(124,58,237,0.7)');

  const dayMap = { Monday: 'Пн', Tuesday: 'Вв', Wednesday: 'Ср', Thursday: 'Чт', Friday: 'Пт', Saturday: 'Сб', Sunday: 'Нд' };
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: days.map(d => dayMap[d]),
      datasets: [
        {
          label: 'ROI (%)',
          data: roi,
          backgroundColor: colors,
          borderRadius: 8,
          borderSkipped: false,
          yAxisID: 'y'
        },
        {
          label: 'Прибуток ($)',
          data: profit,
          type: 'line',
          borderColor: GREEN,
          backgroundColor: 'rgba(34,197,94,0.05)',
          borderWidth: 2,
          fill: true,
          pointBackgroundColor: GREEN,
          pointRadius: 4,
          yAxisID: 'y1',
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'bottom', labels: { usePointStyle: true, padding: 16 } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              if (ctx.dataset.label === 'Прибуток ($)') return ` Прибуток: $${ctx.raw.toLocaleString()}`;
              return ` ROI: ${ctx.raw}%`;
            }
          }
        }
      },
      scales: {
        y: { grid: { color: '#2a2a3a' }, ticks: { callback: v => `${v}%` } },
        y1: { position: 'right', grid: { display: false }, ticks: { callback: v => `$${(v/1000).toFixed(1)}K` } }
      }
    }
  });
}

// === CHART 4: Buyer ROI ===
function drawBuyerChart() {
  const ctx = document.getElementById('buyerChart');
  if (!ctx) return;

  const buyers = Object.keys(DATA.buyers);
  const roi = buyers.map(k => parseFloat(((DATA.buyers[k].profit / DATA.buyers[k].cost) * 100).toFixed(1)));
  const colors = roi.map(r => {
    if (r > 80) return 'rgba(34,197,94,0.85)';
    if (r > 25) return 'rgba(124,58,237,0.75)';
    return 'rgba(245,158,11,0.7)';
  });

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: buyers,
      datasets: [{
        label: 'ROI (%)',
        data: roi,
        backgroundColor: colors,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => ` ROI: ${ctx.raw}%` } }
      },
      scales: {
        x: { grid: { color: '#2a2a3a' }, ticks: { callback: v => `${v}%` } },
        y: { grid: { display: false } }
      }
    }
  });
}

// === CHART 5: Return Reasons ===
function drawReturnChart() {
  const ctx = document.getElementById('returnChart');
  if (!ctx) return;

  const reasons = Object.keys(DATA.returnReasons);
  const costs = reasons.map(r => DATA.returnReasons[r].cost_lost);
  const counts = reasons.map(r => DATA.returnReasons[r].count);
  const labels = reasons.map(r => r.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()));

  const barColors = [RED, ORANGE, YELLOW, BLUE, PURPLE, 'rgba(156,163,175,0.7)'];

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Втрати ($)',
        data: costs,
        backgroundColor: barColors,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const reason = reasons[ctx.dataIndex];
              return [
                ` Втрати: $${ctx.raw.toLocaleString()}`,
                ` Лідів: ${DATA.returnReasons[reason].count}`
              ];
            }
          }
        }
      },
      scales: {
        x: { grid: { color: '#2a2a3a' }, ticks: { callback: v => `$${v.toLocaleString()}` } },
        y: { grid: { display: false } }
      }
    }
  });
}

// === GEO TABLE ===
function buildGeoTable() {
  const table = document.getElementById('geoTable');
  if (!table) return;

  const sorted = Object.entries(DATA.states).sort((a, b) => b[1].profit - a[1].profit);

  const header = document.createElement('thead');
  header.innerHTML = '<tr><th>Штат</th><th>Ліди</th><th>Прибуток</th><th>ROI</th><th>Unsold%</th></tr>';
  table.appendChild(header);

  const tbody = document.createElement('tbody');
  sorted.forEach(([state, d]) => {
    const roi = ((d.profit / d.cost) * 100).toFixed(1);
    const unsoldPct = ((d.unsold / d.leads) * 100).toFixed(1);
    const tr = document.createElement('tr');

    const isDanger = d.profit < 0 || parseFloat(unsoldPct) > 25;
    const isWinner = d.profit > 3000;
    if (isDanger) tr.className = 'danger';
    else if (isWinner) tr.className = 'winner';

    tr.innerHTML = `
      <td><strong>${state}</strong></td>
      <td>${d.leads}</td>
      <td>${d.profit >= 0 ? '+' : ''}$${d.profit.toFixed(0)}</td>
      <td>${roi}%</td>
      <td>${unsoldPct}%${parseFloat(unsoldPct) > 25 ? ' ⚠️' : ''}</td>
    `;
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
}

// === PING-POST ANIMATION ===
function initPingPostAnimation() {
  const stages = document.querySelectorAll('.pp-stage');
  const arrows = document.querySelectorAll('.pp-arrow');

  let current = 0;
  const total = stages.length;

  function highlight() {
    stages.forEach((s, i) => {
      s.style.borderColor = i === current ? '#7c3aed' : '';
      s.style.background = i === current ? 'rgba(124,58,237,0.15)' : '';
      s.style.transform = i === current ? 'translateY(-4px)' : '';
      s.style.boxShadow = i === current ? '0 0 20px rgba(124,58,237,0.4)' : '';
    });
    arrows.forEach((a, i) => {
      const line = a.querySelector('.pp-arrow-line');
      if (line) line.style.background = i < current ? 'linear-gradient(90deg, #22c55e, #16a34a)' : '';
    });
  }

  function advance() {
    current = (current + 1) % total;
    highlight();
  }

  highlight();
  setInterval(advance, 1400);
}

// === NAV ACTIVE LINK ===
function initNavHighlight() {
  const sections = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.nav-link');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -40% 0px' });

  sections.forEach(s => observer.observe(s));
}

// Add active link style
const style = document.createElement('style');
style.textContent = `.nav-link.active { color: var(--text); background: rgba(124,58,237,0.15); }`;
document.head.appendChild(style);

// === SCROLL REVEAL ===
function initScrollReveal() {
  const els = document.querySelectorAll('.card, .kpi-card, .anomaly-card, .winner-card, .competitor-card');
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        obs.unobserve(e.target);
      }
    });
  }, { rootMargin: '0px 0px -60px 0px' });

  els.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    obs.observe(el);
  });
}

// === INIT ALL ===
document.addEventListener('DOMContentLoaded', () => {
  drawSourceChart();
  drawVerticalChart();
  drawDayChart();
  drawBuyerChart();
  drawReturnChart();
  buildGeoTable();
  initPingPostAnimation();
  initNavHighlight();
  initScrollReveal();
});
