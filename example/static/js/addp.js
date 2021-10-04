function addp(){
    var newP = document.createElement('p');
    var text = document.createTextNode('안녕! 숨겨진 텍스트에요.');
    newP.appendChild(text);
    document.getElementById("demo").appendChild(newP);  //p태그를 부모 div에 추가
}