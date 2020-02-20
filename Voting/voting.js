var option1, option2, option3 = 0;
var totalVotes = 0;


function vote(id){
    console.log(id);
    totalVotes += 1;
    updatePoints();
}

function updatePoints(){
    // var percentA = (pointA / totalVotes) * 100;
    // var percentB = (pointB / totalVotes) * 100;
    // var size = percentA + "% " + percentB + "%";

    // document.getElementById("size-one").innerHTML = Math.round(percentA) + '%';
    // document.getElementById("size-two").innerHTML = Math.round(percentB) + '%';
    // document.getElementById("voting-box").style.gridTemplateColumns=  percentA + "% " + percentB + "%";
    // document.getElementById("total-votes").innerHTML = "Total Votes Casted: " + totalVotes;
    // document.getElementById("total-left").innerHTML = "Option A: " + pointA;
    document.getElementById("currentVotes").innerHTML = totalVotes;
}

