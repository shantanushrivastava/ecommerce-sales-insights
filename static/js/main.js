Chart.defaults.font.family = "'Segoe UI', sans-serif";
Chart.defaults.color = '#9ca3af';

const C = ['#2056d1','#0f9b6e','#d97706','#6d5dfc','#e0433a','#70c8de','#c026d3','#059669','#7c3aed','#ea580c'];

const TIP = {
  backgroundColor:'#111827', titleColor:'#6b7280',
  bodyColor:'#f9fafb', bodyFont:{size:13,weight:'700'},
  padding:12, cornerRadius:10, displayColors:false,
  callbacks:{ label: c=>' Rs '+Number(c.raw).toLocaleString('en-IN',{maximumFractionDigits:0}) }
};

document.getElementById('dt').textContent =
  new Date().toLocaleDateString('en-IN',{day:'numeric',month:'long',year:'numeric'});

function show(sec, el) {
  document.getElementById('section-dashboard').style.display = sec==='dashboard' ? 'block' : 'none';
  document.getElementById('section-report').style.display    = sec==='report'    ? 'block' : 'none';
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
}

function cu(el, target, pre='') {
  const dur=1100, t0=performance.now();
  const f = now => {
    const p = Math.min((now-t0)/dur,1);
    const v = target*(1-Math.pow(1-p,3));
    el.textContent = pre + Math.round(v).toLocaleString('en-IN');
    if(p<1) requestAnimationFrame(f);
  };
  requestAnimationFrame(f);
}

fetch('/api/kpis').then(r=>r.json()).then(d=>{
  cu(document.getElementById('k1'), d.total_sales,     'Rs ');
  cu(document.getElementById('k2'), d.total_orders,    '');
  cu(document.getElementById('k3'), d.avg_order_value, 'Rs ');
  cu(document.getElementById('k4'), d.total_customers, '');
});

fetch('/api/sales_by_month').then(r=>r.json()).then(d=>{
  new Chart('cMonthly',{
    type:'line',
    data:{labels:d.labels,datasets:[{
      data:d.values,
      borderColor:'#2056d1',
      backgroundColor(ctx){
        const g=ctx.chart.ctx.createLinearGradient(0,0,0,270);
        g.addColorStop(0,'rgba(32,86,209,0.18)');
        g.addColorStop(1,'rgba(32,86,209,0)');
        return g;
      },
      borderWidth:2.5, fill:true, tension:0.4,
      pointRadius:3, pointHoverRadius:6,
      pointBackgroundColor:'#fff', pointBorderColor:'#2056d1', pointBorderWidth:2
    }]},
    options:{
      responsive:true,
      plugins:{legend:{display:false},tooltip:TIP},
      scales:{
        y:{grid:{color:'#f3f4f6'},border:{display:false},ticks:{callback:v=>'Rs '+(v/1000).toFixed(0)+'K',font:{size:10}}},
        x:{grid:{display:false},border:{display:false},ticks:{font:{size:9},maxRotation:45}}
      }
    }
  });
});

fetch('/api/sales_by_category').then(r=>r.json()).then(d=>{
  new Chart('cCat',{
    type:'doughnut',
    data:{labels:d.labels,datasets:[{data:d.values,backgroundColor:C,borderWidth:3,borderColor:'#fff',hoverOffset:8}]},
    options:{
      responsive:true, cutout:'65%',
      plugins:{
        legend:{position:'bottom',labels:{font:{size:10},padding:12,usePointStyle:true,pointStyleWidth:8}},
        tooltip:{...TIP,callbacks:{label:c=>' Rs '+Number(c.raw).toLocaleString('en-IN',{maximumFractionDigits:0})}}
      }
    }
  });
});

fetch('/api/top_products').then(r=>r.json()).then(d=>{
  new Chart('cProd',{
    type:'bar',
    data:{labels:d.labels,datasets:[{data:d.values,backgroundColor:C,borderRadius:5,borderSkipped:false}]},
    options:{
      indexAxis:'y', responsive:true,
      plugins:{legend:{display:false},tooltip:TIP},
      scales:{
        x:{grid:{color:'#f3f4f6'},border:{display:false},ticks:{callback:v=>(v/1000).toFixed(0)+'K',font:{size:9}}},
        y:{grid:{display:false},border:{display:false},ticks:{font:{size:10}}}
      }
    }
  });
});

fetch('/api/payment_methods').then(r=>r.json()).then(d=>{
  new Chart('cPay',{
    type:'pie',
    data:{labels:d.labels,datasets:[{data:d.values,backgroundColor:C,borderWidth:3,borderColor:'#fff',hoverOffset:8}]},
    options:{
      responsive:true,
      plugins:{
        legend:{position:'bottom',labels:{font:{size:10},padding:10,usePointStyle:true,pointStyleWidth:8}},
        tooltip:{...TIP,callbacks:{label:c=>` ${c.label}: ${c.raw}`}}
      }
    }
  });
});

fetch('/api/top_cities').then(r=>r.json()).then(d=>{
  new Chart('cCity',{
    type:'bar',
    data:{labels:d.labels,datasets:[{
      data:d.values,
      backgroundColor:'rgba(109,93,252,0.12)',
      borderColor:'#6d5dfc', borderWidth:1.5,
      borderRadius:5, borderSkipped:false
    }]},
    options:{
      indexAxis:'y', responsive:true,
      plugins:{legend:{display:false},tooltip:TIP},
      scales:{
        x:{grid:{color:'#f3f4f6'},border:{display:false},ticks:{callback:v=>(v/1000).toFixed(0)+'K',font:{size:9}}},
        y:{grid:{display:false},border:{display:false},ticks:{font:{size:10}}}
      }
    }
  });
});

function dl(fmt) {
  const s=document.getElementById('sd').value;
  const e=document.getElementById('ed').value;
  if(!s||!e){alert('Please select both dates.');return;}
  if(s>e){alert('Start date must be before end date.');return;}
  const t=document.getElementById('toast');
  t.style.display='flex';
  setTimeout(()=>t.style.display='none',3500);
  const a=document.createElement('a');
  a.href=`/api/generate_report?start_date=${s}&end_date=${e}&format=${fmt}`;
  a.click();
}
