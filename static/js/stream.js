$(document).ready(function () {
//partidaBracket.clearCart();
//playerSelect.clearEquipe();

var check = partidaBracket.listCart();
//console.log(check);
    if(check.length == 0 ){
   // console.log('nao possui times');
            createTeam();
    }
    if(check.length != 0 ){
    console.log('possui times');
        for(var i in check) {
        console.log(check[i].status);
            if ( check[i].status === stage){
                        console.log(check[i].status);
                        if (grupos.indexOf(check[i].grupo) === -1) grupos.push(check[i].grupo);
                        }
            if ( check[i].status != stage){

        console.log('campeonato evoluiu')

        }
          }
    }
    displayCart();
})