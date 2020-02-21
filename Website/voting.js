var totalVotes = 0;
var votingBib = {};
var winnerVoting;

function vote(id){
    console.log(votingBib);
    if (id in Object.keys(votingBib)) {
        votingBib[id] +=1
    }
    else {
        votingBib[id] = 0
    };
    totalVotes += 1;
    updatePoints();
}

function updatePoints(){
    winnerVoting = Object.keys(votingBib).reduce(function(a, b){ return votingBib[a] > votingBib[b] ? a : b });
    document.getElementById("currentVotes").innerHTML = totalVotes;
    document.getElementById("Winner").innerHTML = winnerVoting;
    //console.log(votingBib);
}