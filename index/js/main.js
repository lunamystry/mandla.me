function modal() {
  this.square = null;
  this.overlay = null;

  this.open = function (content) {
    this.overlay = document.createElement("div");
    this.overlay.className = "overlay";
    this.square = document.createElement("div");
    this.square.className = "square";
    this.square.Code = this;

    var msg = document.createElement("div");
    msg.className = "msg";
    msg.innerHTML = content;

    this.square.appendChild(msg);

    var closebtn = document.createElement("button");
    closebtn.className = "btn";
    closebtn.onclick = function () {
      this.parentNode.Code.close();
    }
    closebtn.innerHTML = "close";
    this.square.appendChild(closebtn);

    document.body.appendChild(this.overlay);
    document.body.appendChild(this.square);
  }

  this.close = function() {
    if (this.square != null) {
      document.body.removeChild(this.square);
      this.square  = null;
    }
    if (this.overlay != null) {
      document.body.removeChild(this.overlay);
      this.overlay = null;
    }
  }
}

function alert(archorid) {
  var anchor = document.getElementById(archorid);
  this.alertdiv = null;

  this.open = function(message, type) {
    this.alertdiv = document.createElement("div");
    this.alertdiv.className = "alert alert-"+type;
    this.alertdiv.Code = this;

    var msg = document.createElement("div");
    msg.className = "msg";
    msg.innerHTML = type.toUpperCase()+": "+message;

    var closebtn = document.createElement("button");
    closebtn.className = "btn";
    closebtn.onclick = function () {
      this.parentNode.Code.close();
    }
    closebtn.innerHTML = "close";

    this.alertdiv.appendChild(msg);
    this.alertdiv.appendChild(closebtn);
    anchor.appendChild(this.alertdiv);
  }

  this.close = function() {
    if (this.alertdiv != null) {
      anchor.removeChild(this.alertdiv);
      this.alertdiv  = null;
    }
  }
}

function openDialog() {
  var modal = new this.modal();
  modal.open("The Gophers in the House!");
}
