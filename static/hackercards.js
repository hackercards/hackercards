var ws = new WebSocket("ws://" + document.domain + ":5000/ws"),
    name, roundJudge;

function joinGame() {
  var text, button;

  function sendName() {
    name = text.val();
    if (name) {
      $("#game").empty();
      ws.send(name);
    }
  }

  text = $('<input name="playerName" type="text" />');
  button = $('<button name="playerJoin" type="button">Join</button>');
  button.click(sendName);
  $("#game").append(text).append(button);
}

ws.onmessage = function(message) {
  message = JSON.parse(message.data);
  if (message.type === 'join') {
    newHand(message.hand);
  } else if (message.type === 'round_start') {
    startRound(message.category, message.judge);
  } else if (message.type === 'draw') {
    addCard(message.card);
  } else if (message.type === 'display') {
    displayCards(message.cards);
  } else if (message.type === 'round_end') {
    endRound(message.winner, message.card);
  } else {
    console.log('Unknown message type: ' + message.type);
  }
}

ws.onclose = function() {
  console.log("Server disconnected");
  $("#round").empty();
  $("#game").empty().append('<h1>Server disconnected</h1>');
}

function makeCard(card) {
  return '<button class="card" type="button">' + card + '</button>';
}

function newHand(cards) {
  var i, hand;
  hand = $('<div class="cards" id="hand" />');
  for (i = 0; i < cards.length; ++i) {
    hand.append(makeCard(cards[i]));
  }
  $("#game").append('<h1>Your hand:</h1>').append(hand);
}

function startRound(category, judge) {
  var round, submitted = false;
  roundJudge = judge;
  $("#round").empty();
  $("#round").append('<h2>Judge: ' + judge + '</h2>')
    .append('<h2>Category: ' + category + '</h2>');

  if (roundJudge !== name) {
    makeClickable($("#hand"), true);
  }
}

function endRound(winner, card) {
  var hand = $('<div class="cards" id="hand" />');
  hand.append(makeCard(card));
  if (roundJudge === name) {
    makeClickable(hand, false);
  }
  $("#round").append('<h2>' + winner + ' wins with:</h2>').append(hand);
}

function addCard(card) {
  $("#hand").append(makeCard(card));
}

function submitCard(card) {
  ws.send(card);
  $("#round").append('<h2>You submitted: ' + card + '</h2>');
}

function displayCards(cards) {
  var hand, i;
  hand = $('<div class="cards" />');
  for (i = 0; i < cards.length; ++i) {
    hand.append(makeCard(cards[i]));
  }
  $("#round").append('<h1>All cards:</h1>').append(hand);
  if (roundJudge === name) {
    makeClickable(hand, false);
  }
}

function makeClickable(element, disappear) {
  var submitted = false;
  element.children().click(function() {
    var button = $(this);
    if (!submitted) {
      submitted = true;
      submitCard(button.text());
      if (disappear) {
        button.remove();
      }
    }
  });
}

window.onload = joinGame;
