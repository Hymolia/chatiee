(function($){

// set up a username
document.getElementById('username').innerHTML = Cookie.get('username');

// set up enter button press event
$("#message-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#message-post").click();
    } 
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
    // console.log(this.model)
 		$(this.el).html("<a class=\"channel-selector\" href=\"#channels/"+this.model.get('name')+"\">" +this.model.get('name')+ "</a>");
    return this;
 	}
});

// Channels view
var ChannelListView = Backbone.View.extend({
el: $('#sidebar'),

events: {
  'click button#create-channel': 'createChannel'
},
initialize: function(){
	_.bindAll(this, 'render', 'createChannel', 'appendChannel');

  this.collection = new ChannelList();
  this.collection.bind('add', this.appendChannel);
  this.collection.fetch();
  // console.log(this.collection)
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
  // channel.save();
},
appendChannel: function(channel){
  var channelView = new ChannelView({
    model: channel
  });
  $('ul#channel-list', this.el).append(channelView.render().el)
}
});







// Create message model
var Message = Backbone.Model.extend({
  defaults: {
    author: Cookie.get('username'),
    content: '',
    date_created: ''
  },
});

var MessageView = Backbone.View.extend({
  initialize: function(){
      _.bindAll(this,'render');
  },

  render: function(){
    $(this.el).html("<p> <small>"+ this.model.get('date_created') + "</small> <strong> "+ this.model.get('author') +"</strong>"+
                this.model.get('content')+ "<p>");
      return this;
  }
});

// Message list view
var MessageListView = Backbone.View.extend({
el: $('#messages'),

events: {
  'click  button#create-channel': 'createChannel'
},
initialize: function(){
  _.bindAll(this, 'render', 'createChannel');

  this.collection = new ChannelList();
  this.collection.bind('add', this.appendChannel);

  this.render();
},

render: function(){
  var self = this;
  // $('#input-button-wrapper', this.el).append("<button class=\"btn btn-default\" id=\"post\">Post it</button>")
  _(this.collection.models).each(function(message){
    self.appendMessage(message)
  }, this);
},

});











var AppRouter = Backbone.Router.extend({
  routes: {
            "channels/:channel_name": "getConversation",
            "*actions": "defaultRoute" // Backbone will try match the route above first
        }
      });
    var app_router = new AppRouter;


    app_router.on('route:getConversation', function (channel_name) {
        // Note the variable in the route definition being passed in here
        alert( "Get post number " + channel_name );   
    });


    app_router.on('route:defaultRoute', function (actions) {
    });

    var ChannelListView = new ChannelListView();
    Backbone.history.start();

})(jQuery);