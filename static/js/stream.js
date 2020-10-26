
function displayCart() {
var grupos = []
var equipes = []
var equipesStage1= []

var myGeocode = [{{ games|tojson }}];
myGeocode.forEach(function(x, index) {

setTimeout(function(){


x.forEach(function(e,index) {
setTimeout(function(){
 var id = e[0];
        var idsquad = e[3];
        var name = e[4];
        var score_1 = e[11];
        var score_2 = e[12];
        var score_3 = e[13];
        var score_total = parseInt(e[11])+parseInt(e[12])+parseInt(e[13]);
        var score_oitava_1 = e[14];
        var score_oitava_2 = e[15];
        var score_quarta_1 = e[16];
        var score_quarta_2 = e[17];
        var score__total_quarta = parseInt(e[16])+parseInt(e[17]);
        var score_semi_1 = e[18];
        var score_semi_2 = e[19];
        var score__total_semi = parseInt(e[18])+parseInt(e[19]);
        var score_final_1 = e[20];
        var score_final_2 = e[21];
        var score__total_final = parseInt(e[20])+parseInt(e[21]);
        var jogo_ativo = e[26];
        var stream = e[27];
        var grupo = e[22];
        var status = e[9];
        console.log(status)
        if (parseInt(status) === 1){
        //if (grupos.indexOf(grupo) === -1) grupos.push(grupo);
        equipesStage1.push({id,idsquad,name,score_1,score_2,score_3,score_total,score_oitava_1,
score_oitava_2,
score_quarta_1,
score_quarta_2,
score__total_quarta,
score_semi_1,
score_semi_2,
score__total_semi,
score_final_1,
score_final_2,
score__total_final,
jogo_ativo,
stream,
grupo,
status,
posicao})
        }
        var posicao = e[28];
        if (grupos.indexOf(grupo) === -1) grupos.push(grupo);
        equipes.push({id,idsquad,name,score_1,score_2,score_3,score_total,score_oitava_1,
score_oitava_2,
score_quarta_1,
score_quarta_2,
score__total_quarta,
score_semi_1,
score_semi_2,
score__total_semi,
score_final_1,
score_final_2,
score__total_final,
jogo_ativo,
stream,
grupo,
status,
posicao})
}, 5000 * (index + 1));

})

if (grupos.length > 7){
createGruposStage(grupos);
    for (c in grupos){
        for (i in equipes){
            if (equipes[i].grupo === grupos[c] ){
            var soma = parseInt(equipes[i].score_1) + parseInt(equipes[i].score_2) + parseInt(equipes[i].score_3);
                        var li = document.createElement("li");
                        li.setAttribute('id', equipes[i].idsquad);
                        li.setAttribute('class', 'team team-top text-center');
                        li.setAttribute('data-percentage', equipes[i].score_total);
                        var textnode = document.createTextNode(equipes[i].name);
                        li.appendChild(textnode);
                        var span  = document.createElement("span");
                        span.setAttribute('class', 'scoreAx');
                        var textnode1 = document.createTextNode(equipes[i].score_1);
                        span.appendChild(textnode1);
                        var span2  = document.createElement("span");
                        span2.setAttribute('class', 'scoreAx');
                        var textnode2 = document.createTextNode(equipes[i].score_2);
                        span2.appendChild(textnode2);
                        var span3  = document.createElement("span");
                        span3.setAttribute('class', 'scoreAx');
                        var textnode3 = document.createTextNode(equipes[i].score_3);
                        span3.appendChild(textnode3);
                        var span_total  = document.createElement("span");
                        span_total.setAttribute('class', 'scoreA');
                        var textnode_total = document.createTextNode(equipes[i].score_total);
                        span_total.appendChild(textnode_total);
                        li.appendChild(span_total);
                        li.appendChild(span3);
                        li.appendChild(span2);
                        li.appendChild(span);
                        document.getElementById(grupos[c]).appendChild(li);

            }

        }
 sortList(grupos[c]);

    }
}
if(equipesStage1.length != 0){
 for (c in equipesStage1 ){
 console.log('fase Oitavas')
 }
 }



}, 5000 * (index + 1));


})


}

