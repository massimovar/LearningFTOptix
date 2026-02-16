## FT Optix Essentials (ITA)
### ASEM tutorials -> [Link](https://www.asem.it/it/pagina/36/risorse-video.html)

<input type="text" id="videoSearch" onkeyup="filterVideos()" placeholder="🔍 Search videos by title, tag, or topic..." style="width:100%;padding:10px 14px;margin-bottom:16px;border:1px solid #ccc;border-radius:8px;font-size:15px;box-shadow:0 1px 3px rgba(0,0,0,0.08);outline:none;">

<script>
function filterVideos() {
  const query = document.getElementById('videoSearch').value.toLowerCase();
  const items = document.querySelectorAll('.video-item');
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? '' : 'none';
  });
}
</script>

#### 🟢 Getting Started

<div class="video-item">

1. [FactoryTalk® Hub Introduction](https://youtu.be/BVXPn04wZ8M) - 36 min
   `#getting-started` `#platform` `#overview` `#beginner`
</div>

#### 🔵 UI Design & Interaction

<div class="video-item">

2. [Reusable Objects and Aliasing](https://youtu.be/fBJ2xfw6E6g) - 17 min
   `#ui` `#objects` `#aliasing` `#intermediate`
</div>
<div class="video-item">

3. [Events and Commands](https://youtu.be/-RCv5g5qJOg) - 20 min
   `#ui` `#events` `#commands` `#interaction` `#intermediate`
</div>
<div class="video-item">

4. [FT Optix Localization](https://youtu.be/i2S1QgnMweM) - 22 min
   `#ui` `#localization` `#i18n` `#intermediate`
</div>

#### 🟡 Data & Monitoring

<div class="video-item">

5. [DataLogger Configuration](https://www.youtube.com/watch?v=gMJdRrsPy34&t=25s) - 17 min
   `#data` `#logging` `#configuration` `#intermediate`
</div>
<div class="video-item">

6. [Trend Configuration and Management](https://youtu.be/HNSS6cBPB0s?si=qx8HxO1EfYcGcGOk) - 16 min
   `#data` `#trends` `#visualization` `#intermediate`
</div>
<div class="video-item">

7. [Alarm Management, Visualization, and Configuration](https://youtu.be/UWi9UaxPYEg) - 27 min
   `#data` `#alarms` `#monitoring` `#configuration` `#intermediate`
</div>

#### 🟠 Security & Users

<div class="video-item">

8. [User, Groups, and Role Management](https://youtu.be/mqgBHsxT2MA?si=hpGKZ6jYQ-v8l6V7) - 19 min
   `#security` `#users` `#roles` `#permissions` `#intermediate`
</div>

#### 🔴 C# / NetLogic Programming

<div class="video-item">

9. [C# 1 Introduction](https://youtu.be/ZCLcgSGX1YU) - 6 min
   `#csharp` `#netlogic` `#programming` `#beginner`
</div>
<div class="video-item">

10. [C# 2 DesignTime NetLogic](https://youtu.be/DMC5OB__D_c) - 20 min
    `#csharp` `#netlogic` `#design-time` `#intermediate`
</div>
<div class="video-item">

11. [C# 3 RunTime NetLogic](https://youtu.be/EEExU0MsbtI) - 37 min
    `#csharp` `#netlogic` `#runtime` `#advanced`
</div>

#### 🟤 Recipes

<div class="video-item">

12. [Recipe Management](https://youtu.be/G_PphV37cbQ) - 20 min
    `#recipes` `#data` `#management` `#advanced`
</div>

#### 🟣 Advanced Topics
<div class="video-item">

13. [How to update the project if the PLC tags have changed](https://youtu.be/CPDWtU506w8) - 12 min
    `#plc` `#tags` `#maintenance` `#advanced`
</div>
<div class="video-item">

14. [Collaborative HMI Design using FTOptix™ and GitHub](https://youtu.be/6n876o6wXco) - 13 min
    `#collaboration` `#github` `#version-control` `#advanced`
</div>

## Webinars
- ASEM 
  - [Responsive UI](https://www.youtube.com/watch?v=1fI2JVNK3qY&ab_channel=ASEMS.r.l.)
  - [Audit](https://www.youtube.com/watch?v=xaqXtFq0mNc)
- Rockwell Automation
  - [Webinar Series: Revitalize Your HMI Operations](https://www.rockwellautomation.com/en-us/events/webinars/revitalize-your-hmi-operations-webinar-series.html)
  - [Rockwell Youtube channel](https://www.youtube.com/playlist?list=PL3K_BigUXJ1M1-JpRiwIIhzJUbhwtK3yy)
