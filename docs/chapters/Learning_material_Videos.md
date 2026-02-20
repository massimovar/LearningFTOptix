---
layout: default
---

<style>
  .section-intro { color: #656d76; font-size: 15px; margin-bottom: 20px; }
  .vid-hero { text-align: center; margin-bottom: 28px; }
  .vid-hero h2 { font-size: 22px; margin-bottom: 6px; border: none; padding: 0; }
  .vid-section { border: 1px solid #d0d7de; border-radius: 10px; padding: 20px 24px; background: #f6f8fa; box-shadow: 0 1px 3px rgba(0,0,0,.08); margin-bottom: 24px; }
  .vid-section h3 { font-size: 17px; margin: 0 0 12px; border: none; padding: 0; }
  .search-box{width:100%;padding:10px 14px;margin-bottom:12px;border:1px solid #d0d7de;border-radius:8px;font-size:15px;box-shadow:0 1px 2px rgba(0,0,0,.06);outline:none;box-sizing:border-box;background:#fff}
  .search-box:focus{border-color:#0969da;box-shadow:0 0 0 3px rgba(9,105,218,.15)}
  .vid-table{width:100%;border-collapse:collapse;margin-bottom:8px}
  .vid-table th,.vid-table td{padding:8px 10px;border:1px solid #d0d7de;text-align:left}
  .vid-table th{background:#eaeef2;cursor:pointer;user-select:none;white-space:nowrap;font-size:13px}
  .vid-table th:hover{background:#d0d7de}
  .vid-table th .arrow{font-size:11px;margin-left:4px;opacity:.4}
  .vid-table th.sorted .arrow{opacity:1}
  .vid-table tr:hover td{background:#f6f8fa}
  .vid-table td:nth-child(1){text-align:center;width:30px}
  .vid-table td:nth-child(4){text-align:center;white-space:nowrap}
  .vid-table a{color:#0969da;text-decoration:none}
  .vid-table a:hover{text-decoration:underline}
  .tag{background:#ddf4ff;color:#0969da;padding:2px 7px;border-radius:12px;font-size:12px;margin:1px 2px;display:inline-block;white-space:nowrap}
  .no-results{text-align:center;padding:16px;color:#656d76;font-style:italic}
  .ext-link { display: inline-block; margin-top: 4px; color: #0969da; text-decoration: none; font-size: 13px; padding: 3px 10px; border: 1px solid #d0d7de; border-radius: 16px; transition: .15s; }
  .ext-link:hover { background: #ddf4ff; border-color: #0969da; }
</style>

<div class="vid-hero">
  <h2> Video Tutorials</h2>
  <p class="section-intro">Searchable and sortable video library  tutorials, webinars, and deep dives into FTOptix.</p>
</div>

---

<div class="vid-section">

### FT Optix Essentials (ITA)

<a class="ext-link" href="https://www.asem.it/it/pagina/36/risorse-video.html">ASEM Video Resources &rarr;</a>

<br><br>

<input type="text" class="search-box" id="videoSearch" placeholder=" Search by title, section, tag..." oninput="filterTable('videoSearch','videosTable')">

<table class="vid-table" id="videosTable">
<thead>
<tr>
  <th onclick="sortTable('videosTable',0,'num')">#<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th onclick="sortTable('videosTable',1,'text')">Section<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th onclick="sortTable('videosTable',2,'text')">Video<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th onclick="sortTable('videosTable',3,'num')">Duration<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th>Tags</th>
</tr>
</thead>
<tbody>
<tr>
  <td>1</td><td> Getting Started</td>
  <td><a href="https://youtu.be/BVXPn04wZ8M">FactoryTalk&reg; Hub Introduction</a></td>
  <td>36 min</td>
  <td><span class="tag">#hub-login</span> <span class="tag">#entitlements</span> <span class="tag">#runtime-sizing</span> <span class="tag">#device-sizing</span> <span class="tag">#releases</span></td>
</tr>
<tr>
  <td>2</td><td> UI Design</td>
  <td><a href="https://youtu.be/fBJ2xfw6E6g">Reusable Objects and Aliasing</a></td>
  <td>17 min</td>
  <td><span class="tag">#alias</span> <span class="tag">#widget-reuse</span> <span class="tag">#dynamic-binding</span> <span class="tag">#dialog-box</span> <span class="tag">#motor-widget</span></td>
</tr>
<tr>
  <td>3</td><td> UI Design</td>
  <td><a href="https://youtu.be/-RCv5g5qJOg">Events and Commands</a></td>
  <td>20 min</td>
  <td><span class="tag">#native-events</span> <span class="tag">#custom-events</span> <span class="tag">#session-commands</span> <span class="tag">#dialog-box</span> <span class="tag">#user-login</span></td>
</tr>
<tr>
  <td>4</td><td> UI Design</td>
  <td><a href="https://youtu.be/i2S1QgnMweM">FT Optix Localization</a></td>
  <td>22 min</td>
  <td><span class="tag">#language-switch</span> <span class="tag">#dictionaries</span> <span class="tag">#date-time-format</span> <span class="tag">#measurement-units</span> <span class="tag">#unit-mapping</span></td>
</tr>
<tr>
  <td>5</td><td> Data &amp; Monitoring</td>
  <td><a href="https://www.youtube.com/watch?v=gMJdRrsPy34&t=25s">DataLogger Configuration</a></td>
  <td>17 min</td>
  <td><span class="tag">#datalogger</span> <span class="tag">#embedded-database</span> <span class="tag">#grid-display</span> <span class="tag">#sampling-types</span> <span class="tag">#csv-export</span></td>
</tr>
<tr>
  <td>6</td><td> Data &amp; Monitoring</td>
  <td><a href="https://youtu.be/HNSS6cBPB0s?si=qx8HxO1EfYcGcGOk">Trend Configuration and Management</a></td>
  <td>16 min</td>
  <td><span class="tag">#real-time-trend</span> <span class="tag">#y-axes</span> <span class="tag">#datalogger-trend</span> <span class="tag">#database-trend</span> <span class="tag">#emulation</span></td>
</tr>
<tr>
  <td>7</td><td> Data &amp; Monitoring</td>
  <td><a href="https://youtu.be/UWi9UaxPYEg">Alarm Management, Visualization, and Configuration</a></td>
  <td>27 min</td>
  <td><span class="tag">#alarm-config</span> <span class="tag">#alarm-widgets</span> <span class="tag">#event-logger</span> <span class="tag">#csv-export</span> <span class="tag">#netlogic</span></td>
</tr>
<tr>
  <td>8</td><td> Security &amp; Users</td>
  <td><a href="https://youtu.be/mqgBHsxT2MA?si=hpGKZ6jYQ-v8l6V7">User, Groups, and Role Management</a></td>
  <td>19 min</td>
  <td><span class="tag">#authentication</span> <span class="tag">#login-interface</span> <span class="tag">#password-policy</span> <span class="tag">#group-permissions</span> <span class="tag">#runtime-users</span> <span class="tag">#upload-from-device</span></td>
</tr>
<tr>
  <td>9</td><td> C# / NetLogic</td>
  <td><a href="https://youtu.be/ZCLcgSGX1YU">C# 1 Introduction</a></td>
  <td>6 min</td>
  <td><span class="tag">#netlogic-overview</span> <span class="tag">#runtime-netlogic</span> <span class="tag">#designtime-netlogic</span> <span class="tag">#api-docs</span> <span class="tag">#library-scripts</span></td>
</tr>
<tr>
  <td>10</td><td> C# / NetLogic</td>
  <td><a href="https://youtu.be/DMC5OB__D_c">C# 2 DesignTime NetLogic</a></td>
  <td>20 min</td>
  <td><span class="tag">#designtime-netlogic</span> <span class="tag">#visual-studio</span> <span class="tag">#write-log</span> <span class="tag">#make-variable</span> <span class="tag">#script-parameters</span> <span class="tag">#debugging</span></td>
</tr>
<tr>
  <td>11</td><td> C# / NetLogic</td>
  <td><a href="https://youtu.be/EEExU0MsbtI">C# 3 RunTime NetLogic</a></td>
  <td>37 min</td>
  <td><span class="tag">#runtime-netlogic</span> <span class="tag">#async-tasks</span> <span class="tag">#variable-subscription</span> <span class="tag">#ui-interaction</span> <span class="tag">#runtime-objects</span> <span class="tag">#debugging</span></td>
</tr>
<tr>
  <td>12</td><td> Recipes</td>
  <td><a href="https://youtu.be/G_PphV37cbQ">Recipe Management</a></td>
  <td>20 min</td>
  <td><span class="tag">#recipe-editor</span> <span class="tag">#recipe-database</span> <span class="tag">#edit-model</span> <span class="tag">#recipe-controller</span> <span class="tag">#apply-from-db</span> <span class="tag">#import-export</span></td>
</tr>
<tr>
  <td>13</td><td> Advanced</td>
  <td><a href="https://youtu.be/CPDWtU506w8">How to update the project if the PLC tags have changed</a></td>
  <td>12 min</td>
  <td><span class="tag">#tag-import</span> <span class="tag">#plc-model-sync</span> <span class="tag">#from-plc-to-model</span> <span class="tag">#csv-model-export</span> <span class="tag">#library-scripts</span></td>
</tr>
<tr>
  <td>14</td><td> Advanced</td>
  <td><a href="https://youtu.be/6n876o6wXco">Collaborative HMI Design using FTOptix&#x2122; and GitHub</a></td>
  <td>13 min</td>
  <td><span class="tag">#github-setup</span> <span class="tag">#commit</span> <span class="tag">#collaborative-dev</span> <span class="tag">#conflict-resolution</span> <span class="tag">#merge</span></td>
</tr>
</tbody>
</table>

</div>

---

<div class="vid-section">

### Webinars

<input type="text" class="search-box" id="webinarSearch" placeholder=" Search webinars..." oninput="filterTable('webinarSearch','webinarsTable')">

<table class="vid-table" id="webinarsTable">
<thead>
<tr>
  <th onclick="sortTable('webinarsTable',0,'text')">Source<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th onclick="sortTable('webinarsTable',1,'text')">Webinar<span class="arrow">&#x25B2;&#x25BC;</span></th>
  <th>Tags</th>
</tr>
</thead>
<tbody>
<tr>
  <td>ASEM</td>
  <td><a href="https://www.youtube.com/watch?v=1fI2JVNK3qY&ab_channel=ASEMS.r.l.">Responsive UI</a></td>
  <td><span class="tag">#responsive-graphics</span> <span class="tag">#multi-resolution</span> <span class="tag">#device-independent</span> <span class="tag">#web-interface</span></td>
</tr>
<tr>
  <td>ASEM</td>
  <td><a href="https://www.youtube.com/watch?v=xaqXtFq0mNc">Audit</a></td>
  <td><span class="tag">#audit-variables</span> <span class="tag">#signature-workflows</span> <span class="tag">#session-events</span> <span class="tag">#event-logger</span> <span class="tag">#recipe-audit</span></td>
</tr>
<tr>
  <td>Rockwell</td>
  <td><a href="https://www.rockwellautomation.com/en-us/events/webinars.html">Webinar Series: Revitalize Your HMI Operations</a></td>
  <td></td>
</tr>
<tr>
  <td>Rockwell</td>
  <td><a href="https://www.youtube.com/playlist?list=PL3K_BigUXJ1M1-JpRiwIIhzJUbhwtK3yy">Rockwell Youtube channel</a></td>
  <td></td>
</tr>
</tbody>
</table>

</div>

<script>
function filterTable(inputId, tableId) {
  const q = document.getElementById(inputId).value.toLowerCase();
  const rows = document.querySelectorAll('#' + tableId + ' tbody tr');
  let visible = 0;
  rows.forEach(r => {
    const match = r.textContent.toLowerCase().includes(q);
    r.style.display = match ? '' : 'none';
    if (match) visible++;
  });
  let nr = document.querySelector('#' + tableId + ' .no-results-row');
  if (visible === 0) {
    if (!nr) {
      nr = document.createElement('tr');
      nr.className = 'no-results-row';
      const cols = document.querySelectorAll('#' + tableId + ' thead th').length;
      nr.innerHTML = '<td colspan="' + cols + '" class="no-results">No videos match your search.</td>';
      document.querySelector('#' + tableId + ' tbody').appendChild(nr);
    }
    nr.style.display = '';
  } else if (nr) {
    nr.style.display = 'none';
  }
}

const sortState = {};
function sortTable(tableId, colIdx, type) {
  const table = document.getElementById(tableId);
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr:not(.no-results-row)'));
  const key = tableId + '_' + colIdx;
  sortState[key] = !sortState[key];
  const asc = sortState[key];
  table.querySelectorAll('th').forEach(th => th.classList.remove('sorted'));
  table.querySelectorAll('th')[colIdx].classList.add('sorted');
  rows.sort((a, b) => {
    let va = a.cells[colIdx].textContent.trim();
    let vb = b.cells[colIdx].textContent.trim();
    if (type === 'num') {
      va = parseInt(va) || 0;
      vb = parseInt(vb) || 0;
      return asc ? va - vb : vb - va;
    }
    return asc ? va.localeCompare(vb) : vb.localeCompare(va);
  });
  rows.forEach(r => tbody.appendChild(r));
}
</script>