function display()
{
    var all_tr=document.getElementsByTagName("tr")
    for(i=0;i<all_tr.length;i++)
    {
        var tdvl=all_tr[i].getElementsByTagName("td")[0].innerText;
        if(tdvl == ""){
            all_tr[i].style.display="none";
        }
    }
}