var app = getApp();
var util = require('../../utils/util.js')
Page({
  data: {
   
  },
  onLoad: function () {
    app.editTabBar();
    var random = Math.random() * 10;
    var random1 = Math.random() * 2.3;
    var random2 = Math.random() * 3.1;
    
    this.setData({
      random: random.toFixed(2),
      random1: random1.toFixed(2),
      random2: random2.toFixed(2),      
    });
  },

})