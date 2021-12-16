function moveElements()
{
  var moveFrom = document.getElementById("moveFrom").value;
  var moveTo = document.getElementById("moveTo").value;
  var chesspiece = document.getElementById(moveFrom).innerHTML;
  document.getElementById(moveTo).innerHTML = chesspiece ;
  document.getElementById(moveFrom).innerHTML = "&nbsp;" ;
}

function resetBoard()
{
  window.location.reload();
}
