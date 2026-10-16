/**
 * Data charts for Presentation 1: ECharts (server-side SVG) → PNG with sharp.
 *
 * Run:  npm install && npm run build   (in this folder)
 * Reads pnp-job-tracker: data/mart/jobs.json (live) + data/processed/repair/pending_jobs.json (held back), Job Bank only.
 * Writes ../fig_quality.png, which build_slide_figures.py places in the slide 7 figure.
 */
import { readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import * as echarts from "echarts";
import sharp from "sharp";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = resolve(HERE, "..");
const PNP = resolve(HERE, "../../../../../pnp-job-tracker");

const AMBER = "#C19C00", INK = "#222222", INK2 = "#52514e";
const FONT = "Segoe UI";

type Held = { origin?: string; missing: string[] };
const isJobBank = (x: { origin?: string }) => x.origin === "jobbank";
const liveFile = join(PNP, "data/mart/jobs.json");
const live = (JSON.parse(readFileSync(liveFile, "utf-8")) as { origin?: string }[]).filter(isJobBank).length;
const held: Held[] = JSON.parse(readFileSync(join(PNP, "data/processed/repair/pending_jobs.json"), "utf-8")).filter(isJobBank);
const total = live + held.length;
const asOf = statSync(liveFile).mtime.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

const fmt = (n: number) => n.toLocaleString("en-US");

async function render(name: string, width: number, height: number, option: echarts.EChartsOption) {
  const chart = echarts.init(null, null, { renderer: "svg", ssr: true, width, height });
  chart.setOption({ animation: false, backgroundColor: "#ffffff", textStyle: { fontFamily: FONT, color: INK }, ...option });
  const svg = chart.renderToSVGString();
  chart.dispose();
  const file = join(OUT, `${name}.png`);
  await sharp(Buffer.from(svg), { density: 192 }).png().toFile(file);
  console.log("wrote", file);
}

// ---- slide 7: monthly cost, today vs Azure (USD) ----
// Today: hardware ¥8,000 + ¥40,000 at 7.2 CNY/USD spread over 36 months; power ≈ 550 W × 730 h × CAD 0.13/kWh;
// Render = average of the Aug, Sep and Oct 2026 invoices ($21.75, $46.99, $28.40 projected).
// Azure: Azure Retail Prices API, Canada Central, Oct 16 2026, with the usage assumptions in presentation1.md.
{
  const TODAY = "#2a78d6", AZURE = "#eb6834"; // reference categorical slots 1 and 2
  const parts: [string, number, "Today" | "Azure"][] = [
    ["Hardware (3 years)", 185, "Today"], ["Power", 38, "Today"], ["Render", 32, "Today"],
    ["Database", 58, "Azure"], ["Front Door", 42, "Azure"], ["Container Apps", 38, "Azure"],
    ["Other", 35, "Azure"], ["NAT Gateway", 34, "Azure"],
  ];
  const total = (side: string) => parts.filter((p) => p[2] === side).reduce((a, p) => a + p[1], 0);
  console.log(`cost: today $${total("Today")}/mo, Azure $${total("Azure")}/mo`);
  const rows = [...parts].reverse(); // ECharts draws the first category at the bottom
  const series = (side: "Today" | "Azure", color: string) => ({
    name: `${side}: $${total(side)}/month`, type: "bar" as const, barWidth: "62%", barGap: "-100%",
    data: rows.map(([, v, s]) => (s === side ? v : null)),
    itemStyle: { color, borderRadius: [0, 4, 4, 0] },
    label: { show: true, position: "right" as const, fontFamily: FONT, fontSize: 20, color: INK, formatter: "${c}" },
  });
  await render("fig_costs", 1200, 720, {
    title: {
      text: `Monthly cost (USD): today $${total("Today")}, Azure $${total("Azure")}`,
      subtext: "Today also needed about $6,670 of hardware up front, spread here over 3 years",
      left: 10, top: 4,
      textStyle: { fontFamily: FONT, fontSize: 28, fontWeight: "bold", color: INK },
      subtextStyle: { fontFamily: FONT, fontSize: 18, color: INK2 },
    },
    legend: { top: 92, left: 10, itemWidth: 22, itemHeight: 14, textStyle: { fontFamily: FONT, fontSize: 19, color: INK } },
    grid: { left: 230, right: 80, top: 140, bottom: 10 },
    xAxis: { type: "value", show: false },
    yAxis: {
      type: "category", data: rows.map(([n]) => n), axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { fontFamily: FONT, fontSize: 20, color: INK },
    },
    series: [series("Today", TODAY), series("Azure", AZURE)],
  });
}

// ---- slide 9: why postings are incomplete (a posting can miss several fields) ----
{
  const NAME: Record<string, string> = {
    email: "Apply email", body: "Job description", term: "Employment term", hours: "Hours",
    city: "City", province: "Province", noc: "Occupation code", salary: "Salary",
  };
  const count = new Map<string, number>();
  for (const h of held) for (const m of h.missing) count.set(m, (count.get(m) ?? 0) + 1);
  const top = [...count.entries()].sort((a, b) => b[1] - a[1]).slice(0, 4);
  // top to bottom: all postings, missing each field (bars overlap: one posting can miss several), complete
  const COLOR: Record<string, string> = { all: "#2a78d6", email: "#eb6834", body: "#eda100", term: "#e87ba4",
    hours: "#6250d6", done: "#008300" };
  const rows: [string, string, number][] = [
    ["all", "All postings", total],
    ...top.map(([k, v]) => [k, `Missing: ${NAME[k] ?? k}`, v] as [string, string, number]),
    ["done", "Complete, shown on the site", live],
  ].reverse() as [string, string, number][];
  const pct = Math.round((held.length / total) * 100);
  console.log(`Job Bank ${asOf}: ${fmt(total)} postings, ${fmt(live)} live, ${fmt(held.length)} incomplete (${pct}%)`);
  console.log("missing:", top.map(([k, v]) => `${k} ${fmt(v)}`).join(", "));
  await render("fig_quality", 820, 560, {
    title: {
      text: `${fmt(total)} postings, only ${fmt(live)} complete`,
      subtext: `Job Bank, ${asOf}. One posting can miss several fields, so the missing bars overlap.`,
      left: "center", top: 4,
      textStyle: { fontFamily: FONT, fontSize: 28, fontWeight: "bold", color: INK },
      subtextStyle: { fontFamily: FONT, fontSize: 16, color: INK2 },
    },
    grid: { left: 300, right: 90, top: 100, bottom: 10 },
    xAxis: { type: "value", show: false },
    yAxis: {
      type: "category", data: rows.map(([, label]) => label),
      axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { fontFamily: FONT, fontSize: 19, color: INK },
    },
    series: [{
      type: "bar", barWidth: "62%",
      data: rows.map(([k, , v]) => ({ value: v, itemStyle: { color: COLOR[k] ?? "#8A8886" } })),
      itemStyle: { borderRadius: [0, 4, 4, 0] },
      label: { show: true, position: "right", formatter: (p) => fmt(Number(p.value)), fontFamily: FONT, fontSize: 19, color: INK },
    }],
  });
}
