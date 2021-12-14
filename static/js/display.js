function display()
{
    var all_tr=document.getElementsByTagName("tr");
    length = all_tr.length;
    for(i=0;i<length;i++)
    {
        var tdvl=all_tr[i].getElementsByTagName("td")[0].innerText;
        if(tdvl == ""){
            all_tr[i].style.display="none";
        }
    }
    if(all_tr[2].getElementsByTagName("td")[0].innerText == ""){
        all_tr[0].style.display="none";
        all_tr[1].style.display="none";
    }
}