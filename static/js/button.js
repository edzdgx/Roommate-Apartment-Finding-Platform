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
    $("#addDistance").click(function(){
        var num = Number(document.getElementById("num").value);
        if(num < 10){
            num = num + 0.5;
        }
        document.getElementById("num").value = num;
    });
    $("#minusDistance").click(function(){
        var num = Number(document.getElementById("num").value);
        if(num > 0){
            num = num - 0.5;
        }
        document.getElementById("num").value = num;
    });
    $("#addBudget").click(function(){
        var num = Number(document.getElementById("num1").value);
        if(num < 3000){
            num = num + 100;
        }
        document.getElementById("num1").value = num;
    });
    $("#minusBudget").click(function(){
        var num = Number(document.getElementById("num1").value);
        if(num > 1000){
            num = num - 100;
        }
        document.getElementById("num1").value = num;
    });
});