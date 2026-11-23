/* Toy time-adjusted pLCA model — a line-for-line port of labs/papers/bev_plca_toy.py.
   Illustrative numbers only (see the Python file). */
(function(){
const YEARS=[2025,2030,2035,2040,2045,2050];
const P={"powertrains": ["BEV", "PHEV", "HEV", "FCEV"], "production_t": {"BEV": 15.0, "PHEV": 10.0, "HEV": 7.5, "FCEV": 12.5}, "eol_t": 0.3, "kwh_per_km": {"BEV": 0.235, "PHEV": 0.17, "HEV": 0.0, "FCEV": 0.0}, "litre_per_km": {"BEV": 0.0, "PHEV": 0.028, "HEV": 0.06, "FCEV": 0.0}, "kgh2_per_km": {"BEV": 0.0, "PHEV": 0.0, "HEV": 0.0, "FCEV": 0.0105}, "diesel_exhaust_kg_per_l": 2.68, "diesel_supply_kg_per_l": 0.55, "biodiesel_supply_kg_per_l": 1.0, "sizes": {"Small": 0.75, "Medium": 0.9, "Medium SUV": 1.0, "Large SUV": 1.2}, "grid_2025": {"AFR": 0.5, "AUS": 0.47, "CAN": 0.12, "CHI": 0.56, "CSA": 0.15, "EEU": 0.62, "FSU": 0.38, "IND": 0.64, "JPN": 0.4, "MEA": 0.48, "MEX": 0.38, "ODA": 0.43, "SKO": 0.4, "UK": 0.18, "USA": 0.34, "WEU": 0.2}, "region_names": {"AFR": "Africa", "AUS": "Australia & NZ", "CAN": "Canada", "CHI": "China", "CSA": "Central & South America", "EEU": "Eastern Europe", "FSU": "Former Soviet Union", "IND": "India", "JPN": "Japan", "MEA": "Middle East", "MEX": "Mexico", "ODA": "Other developing Asia", "SKO": "South Korea", "UK": "United Kingdom", "USA": "United States", "WEU": "Western Europe"}, "scenarios": ["No scenario", "No climate action", "Baseline (NDCs)", "Ambitious (<2 °C)", "Very ambitious (1.5 °C)"], "rcp": {"No scenario": "static 2025", "No climate action": "SSP2-RCP6.0", "Baseline (NDCs)": "SSP2-RCP4.5", "Ambitious (<2 °C)": "SSP2-RCP2.6", "Very ambitious (1.5 °C)": "SSP2-RCP1.9"}, "grid_factor": {"No scenario": [1, 1, 1, 1, 1, 1], "No climate action": [1, 0.93, 0.87, 0.82, 0.77, 0.72], "Baseline (NDCs)": [1, 0.78, 0.62, 0.52, 0.45, 0.4], "Ambitious (<2 °C)": [1, 0.75, 0.55, 0.4, 0.28, 0.18], "Very ambitious (1.5 °C)": [1, 0.55, 0.28, 0.12, 0.05, 0.0]}, "bio_share": {"No scenario": [0, 0, 0, 0, 0, 0], "No climate action": [0, 0.02, 0.04, 0.06, 0.08, 0.1], "Baseline (NDCs)": [0, 0.04, 0.08, 0.12, 0.16, 0.2], "Ambitious (<2 °C)": [0, 0.08, 0.16, 0.25, 0.33, 0.4], "Very ambitious (1.5 °C)": [0, 0.12, 0.28, 0.42, 0.52, 0.6]}, "h2_kg_per_kg": {"No scenario": [13, 13, 13, 13, 13, 13], "No climate action": [13, 12.5, 12, 11.5, 11, 10.5], "Baseline (NDCs)": [13, 12, 10, 8, 6.5, 5], "Ambitious (<2 °C)": [13, 11.5, 9, 6.5, 4.5, 3.5], "Very ambitious (1.5 °C)": [13, 3, -10, -20, -25, -28]}, "production_2035_factor": 0.77, "efficiency_2035_factor": {"BEV": 0.95, "PHEV": 0.85, "HEV": 0.93, "FCEV": 0.93}};
function interp(s,y){ if(y<=YEARS[0])return s[0]; if(y>=YEARS[5])return s[5]; const i=Math.floor((y-2025)/5), f=(y-YEARS[i])/5; return s[i]+f*(s[i+1]-s[i]); }
function intens(region,sc,y){ const g=P.grid_2025[region]*interp(P.grid_factor[sc],y), b=interp(P.bio_share[sc],y);
  return {grid:g, exhaust:P.diesel_exhaust_kg_per_l*(1-b), supply:P.diesel_supply_kg_per_l*(1-b)+P.biodiesel_supply_kg_per_l*b, h2:interp(P.h2_kg_per_kg[sc],y), bio:b}; }
function footprint(pt,o){ o=Object.assign({region:"CHI",scenario:"Ambitious (<2 °C)",size:"Medium SUV",km:200000,lifetime:15,build_year:2025,uf:null},o||{});
  const s=P.sizes[o.size], late=o.build_year>=2035;
  const prod=P.production_t[pt]*s*(late?P.production_2035_factor:1), eff=s*(late?P.efficiency_2035_factor[pt]:1);
  let kwh=P.kwh_per_km[pt], lit=P.litre_per_km[pt];
  if(pt==="PHEV"&&o.uf!=null){ kwh=0.36*o.uf; lit=0.053*(1-o.uf); }
  kwh*=eff; lit*=eff; const h2=P.kgh2_per_km[pt]*eff, kpy=o.km/o.lifetime;
  let e=0,sup=0,ex=0,hy=0; const yearly=[];
  for(let y=0;y<o.lifetime;y++){ const I=intens(o.region,o.scenario,o.build_year+y+0.5);
    const a=kpy*kwh*I.grid, b=kpy*lit*I.supply, c=kpy*lit*I.exhaust, d=kpy*h2*I.h2; e+=a; sup+=b; ex+=c; hy+=d; yearly.push(a+b+c+d); }
  const parts={"Production":prod*1000,"Electricity":e,"Diesel supply":sup,"Exhaust":ex,"Hydrogen":hy,"End of life":P.eol_t*1000};
  const g={}; let tot=0; for(const k in parts){ g[k]=parts[k]/o.km*1000; tot+=g[k]; }
  return {total:tot, parts:g, kg:parts, yearly:yearly}; }
function breakeven(o){ const f=km=>footprint("BEV",Object.assign({},o,{km})).total-footprint("HEV",Object.assign({},o,{km})).total;
  let lo=1000,hi=1e6; if(f(hi)>0)return null; for(let i=0;i<60;i++){const m=(lo+hi)/2; if(f(m)>0)lo=m; else hi=m;} return hi; }
function rng(seed){ let s=seed>>>0||1; return ()=>{ s^=s<<13; s>>>=0; s^=s>>17; s^=s<<5; s>>>=0; return s/4294967296; }; }
function sample(r,scens){ const R=Object.keys(P.grid_2025), S=Object.keys(P.sizes), sc=scens||P.scenarios;
  return {region:R[Math.floor(r()*R.length)], scenario:sc[Math.floor(r()*sc.length)], size:S[Math.floor(r()*S.length)], km:100000+r()*200000, lifetime:10+Math.floor(r()*11)}; }
window.PLCA={P,YEARS,interp,intens,footprint,breakeven,rng,sample};
})();
