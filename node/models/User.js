const mongoose = require('mongoose')
const bcrypt = require('bcrypt')
const saltRounds = 10

var jwt = require('jsonwebtoken');

const userSchema = mongoose.Schema({
    name:{
        type: String,
        maxlength: 50
    },
    email:{
        type: String,
        trim: true,
        unique: 1
    },
    password:{
        type: String,
        minlength: 5
    },

    role:{
        type: Number,
        default: 0
    },
    image: String,
    token:{
        type: String
    },
    tokenExp:{
        type: Number
    }
})

userSchema.pre('save', function (next) {
    var user = this;


    if (user.isModified('password')) {
        // password bcrypt
        bcrypt.genSalt(saltRounds, function (err, salt) {
            if (err) return next(err)
            bcrypt.hash(user.password, salt, function (err, hash) {
                if (err) return next(err)
                // Store hash in your password DB.
                user.password = hash
                next()
            })
        })
    } else {
        next()
    }
})

userSchema.methods.comparePassword = function(plainPassword, cb){
    // match plain password with DB
    bcrypt.compare(plainPassword, this.password, function(err, isMatch){
        if(err) return cb(err)
        cb(null, isMatch)
    })
}

userSchema.methods.genToken = function(cb){
    var user = this

    // using jsonwebtoken, create token
    // user._id + 'secretToken' = token
    // using secretToken, identify user._id
    var token = jwt.sign(user._id.toHexString(), 'secretToken')
    user.token = token
    user.save(function(err, user){
        if(err) return cb(err)
        cb(null, user)
    })
}

userSchema.statics.findByToken = function(token, cb){
    var user = this

    // decode token
    jwt.verify(token, 'secretToken', function(err, decoded){
        // using userId, find user
        // check whether token from client is same with token of DB
        user.findOne({"_id": decoded, "token": token}, function(err, user){
            if(err) return cb(err)
            cb(null, user)
        })
    })
}

const User = mongoose.model('User', userSchema)

module.exports = { User }