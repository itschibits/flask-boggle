"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure
  for (let row of board){
    let tableRow = $('<tr>')
    $('tbody').append(tableRow)
    for (let cell of row){
      let tableCell = $('<td>').text(cell)
      tableRow.append(tableCell)
    }
  }
}


start();