function verificarSenha(){
    var x = document.getElementsByName("passwordconfirmacao")[0];
    if (x.value == document.getElementsByName("password")[0].value){
        var element = document.getElementById("infosenha");
            element.classList.remove('animated', 'fadeInDown', 'fast');
            element.classList.add('animated', 'fadeOutUp', 'fast');
            element.addEventListener('animationend', function(){
                element.parentNode.removeChild(element);
            });
    }
    else{
        if (!(!!document.getElementById("infosenha"))){
      
        x = x.parentElement.parentElement.parentElement;
        console.log(x);
            var info = document.createElement("div");
            info.classList.add('alert', 'alert-danger', 'animated', 'fadeInDown', 'fast');
            info.setAttribute('role', 'alert');
            info.innerHTML = 'As senhas não coincidem';
            info.id="infosenha";
            x.parentElement.insertBefore(info, x);
    }
    }
}
    function verificarEmail(){
        var x = document.getElementsByName("emailconfirmacao")[0];
        if (String(x.value).toLowerCase() == String(document.getElementsByName("email")[0].value).toLowerCase()){
            var element = document.getElementById("infoemail");
            element.classList.remove('animated', 'fadeInDown', 'fast');
            element.classList.add('animated', 'fadeOutUp', 'fast');
            element.addEventListener('animationend', function(){
                element.parentNode.removeChild(element);
            });
        }
        else{
            if (!(!!document.getElementById("infoemail"))){
                
            x = x.parentElement.parentElement.parentElement;
            var info = document.createElement("div");
            info.classList.add('alert', 'alert-danger', 'animated', 'fadeInDown', 'fast');
            info.setAttribute('role', 'alert');
            info.innerHTML = 'Os emails não coincidem';
            info.id="infoemail";
            x.parentElement.insertBefore(info, x);

            //x.appendChild(info)
        }
        }
        }
var e1 = document.getElementsByName("passwordconfirmacao")[0];
e1.addEventListener("input", verificarSenha);
var e2 = document.getElementsByName("emailconfirmacao")[0];
e2.addEventListener("input", verificarEmail);
var e3 = document.getElementById("formcadastro");
e3.addEventListener("submit", event => {
            var x = document.getElementsByName("emailconfirmacao")[0];
            if (String(x.value).toLowerCase() == String(document.getElementsByName("email")[0].value).toLowerCase()){
                var y = document.getElementsByName("passwordconfirmacao")[0];
                if (y.value == document.getElementsByName("password")[0].value){
                    return true;
                }
            }
            event.preventDefault();
            return false;
    
  });