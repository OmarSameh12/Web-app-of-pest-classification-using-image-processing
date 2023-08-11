let userNameInput = document.getElementById('username');
let emailInput = document.getElementById('email');
let passwordInput = document.getElementById('password1');
let passwordInput2 = document.getElementById('password2');
let SignUpBtn = document.getElementById('SignUpBtn');
let alertMessage = document.getElementById('alertMessage');
let alertMessage1 = document.getElementById('alertMessage1');
let alertMessage2 = document.getElementById('alertMessage2');
let alertMessage3 = document.getElementById('alertMessage3');
let loginBtn = document.getElementById('LoginBtn');
let welcomeMessage = document.getElementById('welcomeMessage');
let LogoutBtn = document.getElementById('LogoutBtn')
let PwRestrictions = document.getElementById('theList')

function renderpage() {
    let title = document.getElementById('title').innerHTML;
    console.log(title);
    if (title == 'Login') {
        rendererrorsLogin();
    }
    else if (title == 'Register') {
        rendererrors();
    }else if (title=='ResetPASS'){
        renderresetpage()
    }
}
function renderresetpage(){
    let flag=document.getElementById('flag').innerHTML;
    if (flag==0){
        emailInput.style.border = ' 3px solid rgb(255, 89, 89)'
        alertMessage3.classList.replace('d-none', 'd-block')
        alertMessage3.innerHTML = "Email entered is not correct"
        alertMessage3.style.color = ' rgb(255, 89, 89)'   
    }
}
function rendererrorsLogin() {
    let flag = document.getElementById('flag').innerHTML;
    if (flag == 0) {
        if(document.getElementById('backerr').innerHTML=='No' ){
            setTimeout(loadprofile(), 6000)  
    }else{
        alertMessage.innerHTML = document.getElementById('backerr').innerHTML
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
    }
}
}


function loadprofile() {
    window.location.href = '/profile';
    xhr.send();

}
var emailCorr=true;
function rendererrors() {
    let flag = document.getElementById('flag').innerHTML;
    if (flag == 0) {
        if (!CheckEmail()) {
            alertMessage.innerHTML = "Email already exist"
            alertMessage.classList.replace('d-none', 'd-block')
            alertMessage.style.color = 'rgb(255, 41, 41)'
            emailCorr=false;
        } else {
            alertMessage1.classList.replace('d-block', 'd-none')
            userNameInput.value = ""
            userNameInput.style.border = "none"
            alertMessage.innerHTML = "Success!"
            alertMessage.classList.replace('d-none', 'd-block')
            alertMessage.style.color = 'rgb(87, 255, 87)'

            setTimeout(loadlogin(), 6000)
        }
    }

}
function loadlogin() {

    window.location.href = '/login';

  

    xhr.send();
}
renderpage();
function Signup() {
    alertMessage.innerHTML = ""
    if (userNameInput.value == '' || emailInput.value == '' || passwordInput.value == '' || passwordInput2.value == '') {
        if (userNameInput.value == '') {
            userNameInput.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage1.classList.replace('d-none', 'd-block')
            alertMessage1.innerHTML = "Name field is required"
            alertMessage1.style.color = ' rgb(255, 89, 89)'
        } else {
            alertMessage1.classList.replace('d-block', 'd-none')
            userNameInput.style.border = "none"
        }
        if (emailInput.value == '') {
            emailInput.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage2.classList.replace('d-none', 'd-block')
            alertMessage2.innerHTML = "Email field is required"
            alertMessage2.style.color = ' rgb(255, 89, 89)'
        } else {
            alertMessage2.classList.replace('d-block', 'd-none')
            emailInput.style.border = "none"
        
    }
        if (passwordInput.value == '') {
            passwordInput.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage3.classList.replace('d-none', 'd-block')
            alertMessage3.innerHTML = "Password field is required"
            alertMessage3.style.color = ' rgb(255, 89, 89)'
        } else {
            alertMessage3.classList.replace('d-block', 'd-none')
            passwordInput.style.border = "none"
        }
        if (passwordInput2.value == '') {
            passwordInput2.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage4.classList.replace('d-none', 'd-block')
            alertMessage4.innerHTML = "Confirm password field is required"
            alertMessage4.style.color = ' rgb(255, 89, 89)'
        } else {
            alertMessage4.classList.replace('d-block', 'd-none')
            passwordInput2.style.border = "none"
        }
        return false;
    }
    if (EmailValidation(emailInput) == false) {
        alertMessage.innerHTML = "Enter Valid Email"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
        emailInput.style.border='red'
        emailCorr=false;
        if (userNameInput.value != '' || emailInput.value != '' || passwordInput.value != '' || passwordInput2.value != '') {
            if (userNameInput.value != '') {
                alertMessage1.classList.replace('d-block', 'd-none')

                userNameInput.style.border = "none"
            }
            if (emailInput.value!= '') {
                if(emailCorr){
                emailInput.style.border = "none"
                  
            }else{
                emailInput.style.border='red';
            }
            
            alertMessage2.classList.replace('d-block', 'd-none')

            }
            if (passwordInput.value != '') {
                alertMessage3.classList.replace('d-block', 'd-none')

                passwordInput.style.border = "none"
            }
            if (passwordInput2.value != '') {
                alertMessage4.classList.replace('d-block', 'd-none')
                passwordInput2.style.border = "none"
            }
        

        }

        return false;
    }
    
    if (passwordInput2.value != passwordInput.value) {
        alertMessage.innerHTML = "These passwords does not match"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
        if (userNameInput.value != '' || emailInput.value != '' || passwordInput.value != '' || passwordInput2.value != '') {
            if (userNameInput.value != '') {
                alertMessage1.classList.replace('d-block', 'd-none')

                userNameInput.style.border = "none"
            }
            if (emailInput.value != '') {
                alertMessage2.classList.replace('d-block', 'd-none')

                emailInput.style.border = "none"
            }
            if (passwordInput.value != '') {
                alertMessage3.classList.replace('d-block', 'd-none')

                passwordInput.style.border = "none"
            }
            if (passwordInput2.value != '') {
                alertMessage4.classList.replace('d-block', 'd-none')
                passwordInput2.style.border = "none"
            }
        }
        return false;

    }
    if (PasswordValidation() == false) {
        alertMessage.innerHTML = "Weak Password!"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
        if (userNameInput.value != '' || emailInput.value != '' || passwordInput.value != '' || passwordInput2.value != '') {
            if (userNameInput.value != '') {
                alertMessage1.classList.replace('d-block', 'd-none')

                userNameInput.style.border = "none"
            }
            if (emailInput.value != '') {
                alertMessage2.classList.replace('d-block', 'd-none')

                emailInput.style.border = "none"
            }
            if (passwordInput.value != '') {
                alertMessage3.classList.replace('d-block', 'd-none')

                passwordInput.style.border = "none"
            }
            if (passwordInput2.value != '') {
                alertMessage4.classList.replace('d-block', 'd-none')
                passwordInput2.style.border = "none"
            }
        }

        return false;
    }


    if (userNameInput.value != '' || emailInput.value != '' || passwordInput.value != '' || passwordInput2.value != '') {
        if (userNameInput.value != '') {
            alertMessage1.classList.replace('d-block', 'd-none')

            userNameInput.style.border = "none"
        }
        if (emailInput.value != '') {
            alertMessage2.classList.replace('d-block', 'd-none')

            emailInput.style.border = "none"
        }
        if (passwordInput.value != '') {
            alertMessage3.classList.replace('d-block', 'd-none')

            passwordInput.style.border = "none"
        }
        if (passwordInput2.value != '') {
            alertMessage4.classList.replace('d-block', 'd-none')
            passwordInput2.style.border = "none"
        }
    }

}



function CheckEmail() {
    let err = document.getElementById('backerr').innerHTML;
    if (err == 'No') {
        return true;
    }
    return false;

}
function EmailValidation() {
    const emaiPattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    if (emailInput.value.match(emaiPattern)) {
        return true;
    }
    return false;

}
function PasswordValidation() {
    const passPattern = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})/
    if (passwordInput.value.match(passPattern)) {
        return true;
    }
    return false;
}
function Login() {

    if (emailInput.value == '' || passwordInput.value == '') {
        alertMessage.innerHTML = "All inputs are required"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'red'
        return false;

    } else if (EmailValidation(emailInput) == false) {
        alertMessage.innerHTML = "Enter Valid Email"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
        /*if (userNameInput.value != '' || emailInput.value != '' || passwordInput.value != '') {
            if (userNameInput.value != '') {
                alertMessage1.classList.replace('d-block', 'd-none')
                
                userNameInput.style.border = "none"
            }
            if (emailInput.value != '') {
                alertMessage2.classList.replace('d-block', 'd-none')
              
                emailInput.style.border = "none"
            }
            if (passwordInput.value != '') {
                alertMessage3.classList.replace('d-block', 'd-none')
            
                passwordInput.style.border = "none"
            }
        }*/
        return false;
    }
    return true;


}

function Logout() {
    window.location.href = 'index.html'
}
function enternewpass() {
    let pass=document.getElementById('pass1').value;
    let pass2=document.getElementById('pass2').value;
    if (pass == '') {
        passwordInput.style.border = ' 3px solid rgb(255, 89, 89)'
        alertMessage3.classList.replace('d-none', 'd-block')
        alertMessage3.innerHTML = "Password field is required"
        alertMessage3.style.color = ' rgb(255, 89, 89)'
        return false;
    } else {
        alertMessage3.classList.replace('d-block', 'd-none')
        passwordInput.style.border = "none"
    }
    if (pass2.value == '') {
        passwordInput2.style.border = ' 3px solid rgb(255, 89, 89)'
        alertMessage2.classList.replace('d-none', 'd-block')
        alertMessage2.innerHTML = "Confirm password field is required"
        alertMessage2.style.color = ' rgb(255, 89, 89)'
        return false;

    } else {
        alertMessage2.classList.replace('d-block', 'd-none')
        pass2.style.border = "none"
    }
    if(pass!=pass2){
        passwordInput2.style.border = ' 3px solid rgb(255, 89, 89)'
        alertMessage2.classList.replace('d-none', 'd-block')
        alertMessage2.innerHTML = "These passwords does not match"
        alertMessage2.style.color = ' rgb(255, 89, 89)'
        return false;
    }if (PasswordValidation() == false) {
        alertMessage.innerHTML = "Weak Password!"
        alertMessage.classList.replace('d-none', 'd-block')
        alertMessage.style.color = 'rgb(255, 41, 41)'
        if (pass != '' || pass2 != '') {

            if (pass != '') {
                alertMessage3.classList.replace('d-block', 'd-none')

                passwordInput.style.border = "none"
            }
            if (pass2 != '') {
                alertMessage2.classList.replace('d-block', 'd-none')
                passwordInput2.style.border = "none"
            }
        }

        return false;
    }

    return true;
}
function resetPass() {
    if (emailInput.value == '') {
        if (emailInput.value == '') {
            emailInput.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage3.classList.replace('d-none', 'd-block')
            alertMessage3.innerHTML = "Email field is required"
            alertMessage3.style.color = ' rgb(255, 89, 89)'
        } else {
            alertMessage3.classList.replace('d-block', 'd-none')
            emailInput.style.border = "none"
        }

        return false;
    }else if (EmailValidation(emailInput.value) == false){
        emailInput.style.border = ' 3px solid rgb(255, 89, 89)'
            alertMessage3.classList.replace('d-none', 'd-block')
            alertMessage3.innerHTML = "Email is not valid"
            alertMessage3.style.color = ' rgb(255, 89, 89)'
            return false;
    }
    return true;
}


const navbar = document.querySelector('.navbar')
window.addEventListener('scroll', () => {
    if (window.scrollY >= 100) {
        navbar.classList.add('navbar-scrolled');
    }
    else if (window.scrollY < 100) {
        navbar.classList.remove('navbar-scrolled');
    }
})
var loadFile = function (event) {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.classList.replace('d-none', 'd-block')
    var uploadtext = document.getElementById('uploadtext')
    var uploadicon = document.getElementById('uploadicon')
    var uploadbutton = document.getElementById('uploadbutton')
    var uploadbg = document.getElementById('uploadbg')
    uploadtext.classList.replace('d-block', 'd-none')
    uploadicon.classList.replace('d-block', 'd-none')
    uploadbutton.classList.replace('d-none', 'd-block')
    uploadbg.classList.add('bg-transparent')

};
function toggleVisibility() {
    var getPasword1 = document.getElementById("password1");
    if (getPasword1.type === "password") {
        getPasword1.type = "text";
    } else {
        getPasword1.type = "password";
    }

}
function toggleVisibility2() {
    var getPasword2 = document.getElementById("password2");
    if (getPasword2.type === "password") {
        getPasword2.type = "text";
    } else {
        getPasword2.type = "password";
    }

}
// Function to open the pop-up window
function openModal(name,commonname,howtocont,value,damage,created_at) {

    let commonnameel=document.getElementById('commonname');
    let nameel=document.getElementById('insectname');
    let howtocontel=document.getElementById('howtocont') ;
    var modal = document.getElementById('myModal');

    if(commonname==''){
        document.getElementById('pest_common_name').hidden=true;
    }
    if(damage==''){
        document.getElementById('Damage_title').hidden=true;
    }
    if(howtocont==''){
        document.getElementById('how_to_cont').hidden
    }
    modal.style.display = 'block';
    
    commonnameel.innerHTML=commonname
    nameel.innerHTML=name
    var splitter = ".";
    let damagel=document.getElementById('damage')
    var damagearr = damage.split(splitter);
    var box='';
    for (let i=0;i<(damagearr.length-1);i++){
        box+=`
            <li>${damagearr[i]}</li>
            `
    } 
    damagel.innerHTML+=box
    box2='';
    var outputArray = howtocont.split(splitter);
    for (let i=0;i<(outputArray.length-1);i++){
             console.log(outputArray[i]);
                box2+=`
                <li>${outputArray[i]}</li>
                `
             
    } 
  
    howtocontel.innerHTML=box2

  
   let imageel=document.getElementById('imageindetail').src=`static/user_pics/${value}`;
    let createdatel=document.getElementById('created_at').innerHTML=created_at
    modal.style.overflow="hidden"
   
}

// Function to close the pop-up window
function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

if (document.getElementById('title').innerHTML=='resultHistory'){
    console.log("here");
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
          event.preventDefault();
        }
      });
}
