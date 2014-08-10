(function($){

// set up a username for sidebar
document.getElementById('username').innerHTML = Cookie.get('username');

// set up enter button press event
$("#message-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#message-post").click();
    } 
});

// Create message model. Use only save()
var Message = Backbone.Model.extend({
  defaults: {
    author: Cookie.get('username'),
    content: '',
    date_created: ''
  },  
  initialize: function(channel){
      this.url = 'channels/'+channel['channel']
  }
});

// Use only fetch()
var MessageList = Backbone.Collection.extend({
  model: Message,

  initialize: function(channel){
      this.url = 'channels/'+channel
  }
})

var MessageView = Backbone.View.extend({
  tagName: 'p',
  initialize: function(){
      _.bindAll(this,'render');
  },

  render: function(){

    $(this.el).html("<small>"+ this.model.get('date_created') + "</small> <strong> "+ this.model.get('author') +":</strong> "+
                this.model.get('content'));
      return this;
  }
});

// Message list view
var MessageListView = Backbone.View.extend({
    el: $('#conversation'),

    events: {
      'click #message-post': 'postMessage'
    },
    initialize: function(channel){
      _.bindAll(this, 'render', 'postMessage', 'appendMessage');
      this.channel = channel
      this.collection = new MessageList(channel.channel_name);
      this.collection.bind('add', this.appendMessage);
      this.collection.fetch()
      this.render();
    },

    render: function(){
      var message_self = this;
        _(this.collection.models).each(function(message){
        message_self.appendMessage(message)
      }, this);
    },

    postMessage: function(e){
      current_channel = arguments[0].currentTarget.getAttribute('channel');
      var message = new Message({"channel": current_channel})
      message.set({
        content: $('#message-input', this.el).val()
      });
      this.collection.add(message)
      message.save();
    },

    appendMessage: function(message){
    var messageView = new MessageView({
      model: message
    });
    $('div#messages', this.el).append(messageView.render().el)
},

});













// Create channel model
var Channel = Backbone.Model.extend({
  urlRoot: 'channels'
});

// Channel collection
var ChannelList = Backbone.Collection.extend({
	model: Channel,
  url: 'channels'
})

// Channel view
var ChannelView = Backbone.View.extend({
	tagName: 'li',
	initialize: function(){
    	_.bindAll(this,'render');
 	},

 	render: function(){
 		$(this.el).html(
      "<a class=\"channel-selector "+this.model.get('name')
      +"\" href=\"#channels/"+
      this.model.get('name')+"\">#" +this.model.get('name')
      + "</a> <button class=\" glyphicon glyphicon-eye-close subscribe-"+ this.model.get('name') +"\"></button>");

    return this;
 	}
});

// Channels view
var ChannelListView = Backbone.View.extend({
el: $('#sidebar'),

events: {
  'click button#create-channel': 'createChannel',
  'click button.glyphicon-eye-open': 'unsubscribe',
  'click button.glyphicon-eye-close': 'subscribe',
},
initialize: function(){
	_.bindAll(this, 'render', 'createChannel', 'appendChannel');

  this.collection = new ChannelList();
  this.collection.bind('add', this.appendChannel);
  this.collection.fetch()
  this.render();
},

render: function(){
  var self = this;
  // $('#input-button-wrapper', this.el).append("<button class=\"btn btn-default\" id=\"post\">Post it</button>")
  _(this.collection.models).each(function(channel){
    self.appendChannel(channel)
  }, this);
},

createChannel: function(){
  var channel = new Channel();
  channel.set({
    name: $('#channel-name', this.el).val()
  });
  this.collection.add(channel)
  channel.save();
},

subscribe: function(ev) {

  // parsing list of classes for channel name
  var channelName
    for (var i=0; i < arguments[0].currentTarget.classList.length; i++) {
        if(arguments[0].currentTarget.classList[i].match("subscribe-")){
                channelName = arguments[0].currentTarget.classList[i].replace("subscribe-", "")
                console.log(channelName)
              }
      }
  
  if ($.post( "user/"+channelName)) {
    $(arguments[0].currentTarget)
                .toggleClass('glyphicon-eye-close glyphicon-eye-open');
   
  }
},

unsubscribe: function(ev) {
  // parsing list of classes for channel name
  var channelName
  for (var i=0; i < arguments[0].currentTarget.classList.length; i++) {
      if(arguments[0].currentTarget.classList[i].match("subscribe-")){
              channelName = arguments[0].currentTarget.classList[i].replace("subscribe-", "")
              console.log(channelName)
            }
    }
  
  $.ajax({
    url: "user/"+channelName,
    type: 'DELETE'
  });
  $(arguments[0].currentTarget)
                .toggleClass('glyphicon-eye-open glyphicon-eye-close');

},

appendChannel: function(channel){
  var channelView = new ChannelView({
    model: channel
  });


  $('ul#channel-list', this.el).append(channelView.render().el)

  $.get("user", function(data) {
   if (data[channel.attributes.name]) {
        $("li button.subscribe-"+channel.attributes.name)
                    .toggleClass('glyphicon-eye-close glyphicon-eye-open');

            $.get(
              "channels/"+channel.attributes.name+"/unread=true",
            function( data ) {
              $("li button.subscribe-"+channel.attributes.name).append(" "+data);
              }
            )
        
   }

  })
},

});

var ChannelListView = new ChannelListView();

var AppRouter = Backbone.Router.extend({
  routes: {
            "channels/:channel_name": "getConversation",
            "*actions": "defaultRoute" // Backbone will try match the route above first
        }
      });
    var app_router = new AppRouter;

    app_router.on('route:getConversation', function (channel_name) {
        // fixme monkey code, normal removal is needed
        //document.getElementById('messages').innerHTML = "";
        document.getElementById("message-form").style.display = "table";
        document.getElementById("message-post").setAttribute('channel', channel_name);
        var messageListView = new MessageListView({'channel_name': channel_name})
    });


    app_router.on('route:defaultRoute', function (actions) {
    });

    Backbone.history.start();

})(jQuery);