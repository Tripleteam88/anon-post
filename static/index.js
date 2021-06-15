// UTC time to local time
dateposted = document.getElementsByClassName("dateposted");
for (i = 0; i < dateposted.length; i++) {
    postDate = `${dateposted[i].innerHTML} GMT`
    var date = new Date(postDate);
    localPostDate = `${date.toDateString()} ${date.toLocaleTimeString()}`
    dateposted[i].innerHTML = localPostDate
}