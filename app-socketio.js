(function() {
    var $form = $('form');
    var $input = $('input[type=text]');
    var $output = $('div#output');

    var socket = io.connect('/chat');

    socket.on('chat', function(msg) {
        $output.html($output.html() + '<br>' + msg);
    });
    socket.on('connect', function() {
        console.log('Connect', socket.socket.transport.name);
    });
    $form.submit(function(ev) {
        ev.preventDefault();
        socket.emit('chat', $input.val());
        console.log('emitted', $input.val());
        $input.val('');
        return false;
    });
    console.log('init done');

})();