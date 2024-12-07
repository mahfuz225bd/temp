// To search the sub-apps list
document.querySelector("input#search").addEventListener("keyup", (ev) => {
  let searchTerm = ev.target.value.toLowerCase();
  let appItems = document.getElementsByClassName("app-item");

  for (let i = 0; i < appItems.length; i++) {
    let appName = appItems[i].textContent || appItems[i].innerText;
    if (appName.toLowerCase().includes(searchTerm)) {
      appItems[i].style.display = "";
    } else {
      appItems[i].style.display = "none";
    }
  }
});
