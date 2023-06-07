const logout = document.querySelector('#logout');
function popLink(){
    confirm('Are you sure you want to log out?')
}
logout.addEventListener('click',popLink)

document.querySelector('.submit').addEventListener('click',function submit(){
    confirm('Are you sure you want to SUBMIT?')
})