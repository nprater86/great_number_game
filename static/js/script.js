inputNum = document.getElementById('inputNum');
goBtn = document.getElementById('go');
numForm = document.getElementById('numInput');

goBtn.onclick = () => {
    if(inputNum.value === ''){
        event.preventDefault();
        alert('Please enter a number!');
    } else if (inputNum.value > 100 || inputNum.value < 1){
        event.preventDefault();
        alert('Please enter a number between 1 and 100!');
        inputNum.value = '';
    }
} 
