(function($){

var Message = Backbone.Model.extend({
  defaults: {
  	author: '',
  	content: '',
  	// date_created: new Date()
  },
  urlRoot: 'default/postmessage'
  
});

var MessageList = Backbone.Collection.extend({
	model: Message
})

var MessageView = Backbone.View.extend({
	tagName: 'p',
	initialize: function(){
    	_.bindAll(this,'render');
 	},

 	render: function(){
    current_datetime = new Date();
    current_time = current_datetime.getHours()+ ":" + current_datetime.getMinutes() + ":" + current_datetime.getSeconds();
 		$(this.el).html('<small>'+current_time+
 			'</small> <strong>'+this.model.get('author')+'</strong> '+this.model.get('content'));
    	return this;
 	}
});

var ListView = Backbone.View.extend({
el: $('#conversation'),

events: {
  'click button#post': 'postMessage'
},
initialize: function(){
	_.bindAll(this, 'render', 'postMessage');

  this.collection = new MessageList();
  this.collection.bind('add', this.appendMessage);

  this.render();
},

render: function(){
  var self = this;
  $('#form-message', this.el).append("<button id=\"post\" \">Post it</button>")
  _(this.collection.models).each(function(message){
    self.appendMessage(message)
  }, this);
},

postMessage: function(){
//   setInterval(function(){
//     alert('Hello, world!')},500)

  var message = new Message();
  message.set({
    author: 'contentBackbone',
    content: $('#message-input', this.el).val()
  });
  this.collection.add(message)
},
appendMessage: function(message){
  var messageView = new MessageView({
    model: message
  });
  $('#messages', this.el).append(messageView.render().el)
  message.save();
}
});

var listView = new ListView();
})(jQuery);