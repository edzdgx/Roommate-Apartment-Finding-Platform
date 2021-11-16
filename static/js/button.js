$(function(){
    $("#roommateYes").click(function(){
        document.getElementById("Need roommates").style.display="block";
    });
    $("#roommateNo").click(function(){
        document.getElementById("Need roommates").style.display="none";
    });
    $("#certainYes").click(function(){
        document.getElementById("Have a certain choice").style.display="block";
        document.getElementById("Don't Have a certain choice").style.display="none";
    });
    $("#certainNo").click(function(){
        document.getElementById("Have a certain choice").style.display="none";
        document.getElementById("Don't Have a certain choice").style.display="block";
    });
});