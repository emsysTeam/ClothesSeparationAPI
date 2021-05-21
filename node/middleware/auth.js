const { User } = require('../models/User')

let auth = (req, res, next)=>{
    // auth process

    // get token from client
    let token = req.cookies.x_auth;

    // decode token, find user using decoded token
    User.findByToken(token, (err, user)=>{
        if(err) throw err

        // if no user, No
        if(!user) return res.json({ isAuth: false, error: true })

        // if user exist, Okay
        req.token = token
        req.user = user
        next()
    })
}

module.exports = { auth }