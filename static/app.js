/**
 * ChurnGuard-ML Frontend Application Controller
 * Author: Sumarjana Biswas (sumarjanabiswas690@gmail.com)
 * Repository: https://github.com/sumarjanabiswas/Machine-Learning-Development-Plan
 */

const API_BASE = window.location.origin;

// -----------------------------------------------------------------------------
// Presets Data
// -----------------------------------------------------------------------------
const PRESETS = {
  highRisk: {
    account_id: "ACC-CRIT-9921",
    tenure_months: 7,
    contract_arr: 14400.0,
    contract_tier: "Growth",
    industry: "Technology",
    billing_cycle: "Monthly",
    licensed_seats: 25,
    active_seats: 8,
    trailing_30d_logins: 6,
    trailing_90d_logins: 140,
    api_calls_30d: 850,
    feature_exports_30d: 2,
    storage_used_gb: 18.5,
    open_escalated_tickets: 3,
    avg_resolution_hours: 64.0,
    monthly_ticket_minutes: 240.0,
    csat_score: 1.0
  },
  moderate: {
    account_id: "ACC-DRIFT-4012",
    tenure_months: 18,
    contract_arr: 18000.0,
    contract_tier: "Growth",
    industry: "Finance",
    billing_cycle: "Monthly",
    licensed_seats: 40,
    active_seats: 22,
    trailing_30d_logins: 28,
    trailing_90d_logins: 120,
    api_calls_30d: 3200,
    feature_exports_30d: 9,
    storage_used_gb: 45.0,
    open_escalated_tickets: 1,
    avg_resolution_hours: 38.0,
    monthly_ticket_minutes: 110.0,
    csat_score: 3.0
  },
  healthy: {
    account_id: "ACC-PWR-1002",
    tenure_months: 38,
    contract_arr: 54000.0,
    contract_tier: "Enterprise",
    industry: "Healthcare",
    billing_cycle: "Annual",
    licensed_seats: 120,
    active_seats: 115,
    trailing_30d_logins: 135,
    trailing_90d_logins: 360,
    api_calls_30d: 18400,
    feature_exports_30d: 48,
    storage_used_gb: 210.0,
    open_escalated_tickets: 0,
    avg_resolution_hours: 14.0,
    monthly_ticket_minutes: 35.0,
    csat_score: 5.0
  }
};

// Batch Demonstration Accounts
const DEFAULT_BATCH = [
  {
    account_id: "ACC-101",
    tenure_months: 6,
    contract_arr: 12000.0,
    contract_tier: "Growth",
    industry: "Technology",
    billing_cycle: "Monthly",
    licensed_seats: 25,
    active_seats: 6,
    trailing_30d_logins: 8,
    trailing_90d_logins: 130,
    api_calls_30d: 900,
    feature_exports_30d: 3,
    storage_used_gb: 22.0,
    open_escalated_tickets: 3,
    avg_resolution_hours: 58.0,
    monthly_ticket_minutes: 220.0,
    csat_score: 1.0
  },
  {
    account_id: "ACC-102",
    tenure_months: 24,
    contract_arr: 2400.0,
    contract_tier: "Starter",
    industry: "Retail",
    billing_cycle: "Annual",
    licensed_seats: 10,
    active_seats: 9,
    trailing_30d_logins: 32,
    trailing_90d_logins: 90,
    api_calls_30d: 1400,
    feature_exports_30d: 7,
    storage_used_gb: 15.0,
    open_escalated_tickets: 0,
    avg_resolution_hours: 12.0,
    monthly_ticket_minutes: 25.0,
    csat_score: 4.0
  },
  {
    account_id: "ACC-103",
    tenure_months: 14,
    contract_arr: 16000.0,
    contract_tier: "Growth",
    industry: "Finance",
    billing_cycle: "Monthly",
    licensed_seats: 35,
    active_seats: 18,
    trailing_30d_logins: 22,
    trailing_90d_logins: 110,
    api_calls_30d: 2800,
    feature_exports_30d: 8,
    storage_used_gb: 48.0,
    open_escalated_tickets: 1,
    avg_resolution_hours: 42.0,
    monthly_ticket_minutes: 140.0,
    csat_score: 2.0
  },
  {
    account_id: "ACC-104",
    tenure_months: 46,
    contract_arr: 72000.0,
    contract_tier: "Enterprise",
    industry: "Healthcare",
    billing_cycle: "Annual",
    licensed_seats: 180,
    active_seats: 172,
    trailing_30d_logins: 210,
    trailing_90d_logins: 580,
    api_calls_30d: 32000,
    feature_exports_30d: 92,
    storage_used_gb: 340.0,
    open_escalated_tickets: 0,
    avg_resolution_hours: 10.0,
    monthly_ticket_minutes: 18.0,
    csat_score: 5.0
  },
  {
    account_id: "ACC-105",
    tenure_months: 9,
    contract_arr: 1200.0,
    contract_tier: "Starter",
    industry: "Manufacturing",
    billing_cycle: "Monthly",
    licensed_seats: 8,
    active_seats: 3,
    trailing_30d_logins: 5,
    trailing_90d_logins: 60,
    api_calls_30d: 350,
    feature_exports_30d: 1,
    storage_used_gb: 8.0,
    open_escalated_tickets: 2,
    avg_resolution_hours: 52.0,
    monthly_ticket_minutes: 160.0,
    csat_score: 2.0
  }
];

// -----------------------------------------------------------------------------
// Initialization & Tab Handling
// -----------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupPresets();
  setupLiveDomainSignals();
  checkApiHealth();
  
  // Load High Risk preset by default for immediate demonstration
  applyPreset("highRisk");
  
  // Submit single prediction form
  const form = document.getElementById("predict-form");
  if (form) {
    form.addEventListener("submit", handleSinglePredict);
  }
  
  // Batch predict trigger
  const batchBtn = document.getElementById("run-batch-btn");
  if (batchBtn) {
    batchBtn.addEventListener("click", handleBatchPredict);
  }
});

function setupTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add("active");
      }
    });
  });
}

function setupPresets() {
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const presetKey = btn.getAttribute("data-preset");
      applyPreset(presetKey);
    });
  });
}

function applyPreset(key) {
  const data = PRESETS[key];
  if (!data) return;
  
  for (const [k, v] of Object.entries(data)) {
    const el = document.getElementById(k);
    if (el) {
      el.value = v;
    }
  }
  updateDomainSignals();
  triggerPrediction();
}

function setupLiveDomainSignals() {
  const inputs = [
    "trailing_30d_logins", "trailing_90d_logins",
    "active_seats", "licensed_seats",
    "open_escalated_tickets", "avg_resolution_hours", "csat_score"
  ];
  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updateDomainSignals);
    }
  });
}

function updateDomainSignals() {
  const t30 = parseFloat(document.getElementById("trailing_30d_logins")?.value) || 0;
  const t90 = parseFloat(document.getElementById("trailing_90d_logins")?.value) || 1;
  const activeSeats = parseFloat(document.getElementById("active_seats")?.value) || 0;
  const licensedSeats = parseFloat(document.getElementById("licensed_seats")?.value) || 1;
  const openEsc = parseFloat(document.getElementById("open_escalated_tickets")?.value) || 0;
  const resHours = parseFloat(document.getElementById("avg_resolution_hours")?.value) || 0;
  const csat = parseFloat(document.getElementById("csat_score")?.value) || 3.5;
  
  // 1. Velocity Ratio: t30 / (t90 / 3)
  const exp30 = (t90 / 3.0) + 0.0001;
  const velocity = (t30 / exp30).toFixed(2);
  const vEl = document.getElementById("signal-velocity");
  if (vEl) {
    vEl.textContent = `${velocity}x`;
    vEl.style.color = velocity < 0.70 ? "#F43F5E" : (velocity < 1.0 ? "#F59E0B" : "#10B981");
  }
  
  // 2. Seat Saturation Ratio
  const seatSat = ((activeSeats / Math.max(licensedSeats, 1)) * 100).toFixed(0);
  const sEl = document.getElementById("signal-seats");
  if (sEl) {
    sEl.textContent = `${seatSat}%`;
    sEl.style.color = seatSat < 50 ? "#F43F5E" : (seatSat < 75 ? "#F59E0B" : "#10B981");
  }
  
  // 3. Friction Index: (Open * 3) + (Hours / 24) + (1 if CSAT < 3 else 0)
  const csatPenalty = csat < 3.0 ? 1.0 : 0.0;
  const friction = ((openEsc * 3.0) + (resHours / 24.0) + csatPenalty).toFixed(1);
  const fEl = document.getElementById("signal-friction");
  if (fEl) {
    fEl.textContent = friction;
    fEl.style.color = friction > 6.0 ? "#F43F5E" : (friction > 3.0 ? "#F59E0B" : "#10B981");
  }
}

// -----------------------------------------------------------------------------
// Single Account Inference Handler
// -----------------------------------------------------------------------------
async function handleSinglePredict(e) {
  if (e) e.preventDefault();
  triggerPrediction();
}

async function triggerPrediction() {
  const payload = collectFormData();
  const jsonReqEl = document.getElementById("json-request");
  if (jsonReqEl) {
    jsonReqEl.textContent = JSON.stringify(payload, null, 2);
  }
  
  const submitBtn = document.getElementById("btn-submit-predict");
  if (submitBtn) {
    submitBtn.innerHTML = `<span>Scoring Telemetry...</span>`;
    submitBtn.disabled = true;
  }
  
  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "API returned error");
    }
    
    const result = await res.json();
    renderPredictionResult(result);
  } catch (err) {
    console.warn("API request error, using client-side fallback simulation:", err);
    // Client-side fallback calculation matching champion calibrated model
    const mockProb = computeClientSideRisk(payload);
    renderPredictionResult({
      account_id: payload.account_id,
      churn_probability: mockProb,
      risk_tier: mockProb >= 0.35 ? "High" : (mockProb >= 0.20 ? "Medium" : "Low"),
      action_required: mockProb >= 0.35,
      recommended_action: mockProb >= 0.35 ?
        "Priority 1: Trigger Executive CSM Retention Outreach. Investigate escalated tickets immediately." :
        (mockProb >= 0.20 ? "Priority 2: Enroll in Automated Re-engagement Flow & Proactive Check-in." : "Standard Cadence: Account healthy.")
    });
  } finally {
    if (submitBtn) {
      submitBtn.innerHTML = `
        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
        <span>Evaluate Churn Propensity</span>
      `;
      submitBtn.disabled = false;
    }
  }
}

function collectFormData() {
  return {
    account_id: document.getElementById("account_id")?.value || "ACC-1000",
    tenure_months: parseInt(document.getElementById("tenure_months")?.value) || 12,
    contract_arr: parseFloat(document.getElementById("contract_arr")?.value) || 12000.0,
    contract_tier: document.getElementById("contract_tier")?.value || "Growth",
    industry: document.getElementById("industry")?.value || "Technology",
    billing_cycle: document.getElementById("billing_cycle")?.value || "Monthly",
    licensed_seats: parseInt(document.getElementById("licensed_seats")?.value) || 25,
    active_seats: parseInt(document.getElementById("active_seats")?.value) || 15,
    trailing_30d_logins: parseInt(document.getElementById("trailing_30d_logins")?.value) || 30,
    trailing_90d_logins: parseInt(document.getElementById("trailing_90d_logins")?.value) || 100,
    api_calls_30d: parseInt(document.getElementById("api_calls_30d")?.value) || 2500,
    feature_exports_30d: parseInt(document.getElementById("feature_exports_30d")?.value) || 8,
    storage_used_gb: parseFloat(document.getElementById("storage_used_gb")?.value) || 25.0,
    open_escalated_tickets: parseInt(document.getElementById("open_escalated_tickets")?.value) || 0,
    avg_resolution_hours: parseFloat(document.getElementById("avg_resolution_hours")?.value) || 24.0,
    monthly_ticket_minutes: parseFloat(document.getElementById("monthly_ticket_minutes")?.value) || 60.0,
    csat_score: parseFloat(document.getElementById("csat_score")?.value) || 3.0
  };
}

function renderPredictionResult(result) {
  const prob = result.churn_probability;
  const pct = (prob * 100).toFixed(1);
  
  // 1. Update Gauge Text
  const valEl = document.getElementById("gauge-value");
  if (valEl) valEl.textContent = `${pct}%`;
  
  // 2. Animate SVG Gauge Arc
  const fillArc = document.getElementById("gauge-arc");
  if (fillArc) {
    // 283 is semi-circle circumference (pi * r = 3.14159 * 90 = ~283)
    const offset = 283 - (283 * Math.min(prob, 1.0));
    fillArc.style.strokeDashoffset = offset;
    
    if (prob >= 0.35) {
      fillArc.style.stroke = "var(--accent-rose)";
    } else if (prob >= 0.20) {
      fillArc.style.stroke = "var(--accent-amber)";
    } else {
      fillArc.style.stroke = "var(--accent-emerald)";
    }
  }
  
  // 3. Update Risk Tier Banner
  const banner = document.getElementById("risk-banner");
  if (banner) {
    banner.className = `risk-banner tier-${result.risk_tier.toLowerCase()}`;
    const titleEl = document.getElementById("risk-tier-title");
    const statusEl = document.getElementById("risk-tier-status");
    if (titleEl) {
      titleEl.innerHTML = `${result.risk_tier.toUpperCase()} RISK TIER`;
    }
    if (statusEl) {
      statusEl.textContent = result.action_required ? "ACTION REQUIRED" : "MONITOR CADENCE";
    }
  }
  
  // 4. Update Playbook Guidance
  const playbookEl = document.getElementById("playbook-guidance");
  if (playbookEl) {
    playbookEl.textContent = result.recommended_action;
  }
  
  // 5. Update JSON response preview
  const jsonRespEl = document.getElementById("json-response");
  if (jsonRespEl) {
    jsonRespEl.textContent = JSON.stringify(result, null, 2);
  }
}

// -----------------------------------------------------------------------------
// Batch Scoring Handler
// -----------------------------------------------------------------------------
async function handleBatchPredict() {
  const btn = document.getElementById("run-batch-btn");
  if (btn) {
    btn.textContent = "Scoring Batch...";
    btn.disabled = true;
  }
  
  try {
    const res = await fetch(`${API_BASE}/batch_predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accounts: DEFAULT_BATCH })
    });
    
    let data;
    if (res.ok) {
      data = await res.json();
    } else {
      data = simulateBatchResult(DEFAULT_BATCH);
    }
    renderBatchTable(data);
  } catch (err) {
    console.warn("Batch API unavailable, rendering simulated batch:", err);
    renderBatchTable(simulateBatchResult(DEFAULT_BATCH));
  } finally {
    if (btn) {
      btn.textContent = "Score All Accounts";
      btn.disabled = false;
    }
  }
}

function renderBatchTable(data) {
  // Update KPI counters
  document.getElementById("kpi-total").textContent = data.total_accounts;
  document.getElementById("kpi-high").textContent = data.high_risk_count;
  document.getElementById("kpi-med").textContent = data.medium_risk_count;
  document.getElementById("kpi-low").textContent = data.low_risk_count;
  
  const savedARR = (data.high_risk_count * 0.35 * 8400).toLocaleString();
  document.getElementById("kpi-arr").textContent = `$${savedARR}`;
  
  const tbody = document.getElementById("batch-table-body");
  if (!tbody) return;
  tbody.innerHTML = "";
  
  data.predictions.forEach(p => {
    const tr = document.createElement("tr");
    const pct = (p.churn_probability * 100).toFixed(1);
    
    let color = "#10B981";
    let badgeClass = "tier-low";
    if (p.risk_tier === "High") {
      color = "#F43F5E";
      badgeClass = "tier-high";
    } else if (p.risk_tier === "Medium") {
      color = "#F59E0B";
      badgeClass = "tier-medium";
    }
    
    tr.innerHTML = `
      <td style="font-weight:700; font-family:var(--font-mono);">${p.account_id}</td>
      <td>
        <span class="badge ${badgeClass}" style="padding:3px 9px; font-size:11px;">
          ${p.risk_tier}
        </span>
      </td>
      <td>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width:${pct}%; background:${color};"></div>
        </div>
        <span style="font-weight:700; font-family:var(--font-mono);">${pct}%</span>
      </td>
      <td>
        <span style="color: ${p.action_required ? '#F43F5E' : '#94A3B8'}; font-weight:600;">
          ${p.action_required ? '● Outreach Triggered' : '○ Standby'}
        </span>
      </td>
      <td style="font-size:12px; color:var(--text-secondary); max-width:320px; overflow:hidden; text-overflow:ellipsis;">
        ${p.recommended_action}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function simulateBatchResult(accounts) {
  const preds = accounts.map(acc => {
    const prob = computeClientSideRisk(acc);
    return {
      account_id: acc.account_id,
      churn_probability: prob,
      risk_tier: prob >= 0.35 ? "High" : (prob >= 0.20 ? "Medium" : "Low"),
      action_required: prob >= 0.35,
      recommended_action: prob >= 0.35 ?
        "Priority 1: Immediate CSM Retention Intervention." :
        (prob >= 0.20 ? "Priority 2: Re-engagement & Onboarding Check-in." : "Standard Cadence: Healthy account.")
    };
  });
  
  return {
    total_accounts: preds.length,
    high_risk_count: preds.filter(p => p.risk_tier === "High").length,
    medium_risk_count: preds.filter(p => p.risk_tier === "Medium").length,
    low_risk_count: preds.filter(p => p.risk_tier === "Low").length,
    predictions: preds
  };
}

// -----------------------------------------------------------------------------
// System Health Check
// -----------------------------------------------------------------------------
async function checkApiHealth() {
  const badge = document.getElementById("health-badge");
  const latencyEl = document.getElementById("api-latency");
  const start = performance.now();
  
  try {
    const res = await fetch(`${API_BASE}/health`);
    const end = performance.now();
    const latency = Math.round(end - start);
    
    if (res.ok) {
      const data = await res.json();
      if (badge) {
        badge.innerHTML = `<span class="pulse-dot"></span> API ${data.status}`;
      }
      if (latencyEl) latencyEl.textContent = `${latency}ms`;
      
      const vEl = document.getElementById("spec-version");
      if (vEl) vEl.textContent = data.model_version;
      const tEl = document.getElementById("spec-threshold");
      if (tEl) tEl.textContent = `t* = ${data.decision_threshold}`;
      const fEl = document.getElementById("spec-features");
      if (fEl) fEl.textContent = `${data.features_monitored} Features`;
    }
  } catch (err) {
    if (badge) {
      badge.innerHTML = `<span class="pulse-dot" style="background:#F59E0B; box-shadow:0 0 10px #F59E0B;"></span> Local Engine`;
    }
  }
}

// -----------------------------------------------------------------------------
// Client-Side Fallback Logistic Estimator
// -----------------------------------------------------------------------------
function computeClientSideRisk(p) {
  const exp30 = (p.trailing_90d_logins / 3.0) + 0.0001;
  const velocity = p.trailing_30d_logins / exp30;
  const sat = p.active_seats / Math.max(p.licensed_seats, 1);
  const csat = p.csat_score !== null ? p.csat_score : 3.5;
  
  const logit = (
    - 2.80
    - 1.40 * (velocity - 1.0)
    + 0.55 * p.open_escalated_tickets
    + 0.018 * (p.avg_resolution_hours - 20.0)
    - 0.45 * (csat - 3.0)
    - 0.025 * (p.tenure_months - 18.0)
    + (p.billing_cycle === 'Monthly' ? 0.40 : 0.0)
    - (p.contract_tier === 'Enterprise' ? 0.35 : 0.0)
    - 0.50 * (sat - 0.70)
  );
  
  const prob = 1.0 / (1.0 + Math.exp(-logit));
  return Math.max(0.01, Math.min(0.99, parseFloat(prob.toFixed(4))));
}
