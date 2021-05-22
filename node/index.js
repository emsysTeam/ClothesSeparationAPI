const express = require('express')
const app = express()
const port = 5000
const path = require('path')
const cookieParser = require('cookie-parser')

const config = require('./config/key')

const { auth } = require('./middleware/auth')
const { User } = require('./models/User')

const mongoose = require('mongoose')
const { response } = require('express')
mongoose.connect(config.mongoURI, {
  useNewUrlParser: true, useUnifiedTopology: true, useCreateIndex: true, useFindAndModify: false
}).then(() => console.log('MongoDB Connected...'))
  .catch(err => console.log(err))

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser())
app.get('/', (req, res) => {
  // res.send('Hello World!!')
  // res.sendFile('views/login.html');
  res.sendFile(path.join(__dirname, "./views/main.html"));
})

app.post('/api/users/register', (req, res) => {
  // get information from clinet, insert infromation into database
  const user = new User(req.body)
  user.save((err, userInfo) => {
    if (err) return res.json({ success: false, err })
    return res.status(200).json({
      success: true
    })
  })
})

app.get('/api/users/login', (req, res)=>{
  res.sendFile(path.join(__dirname, "./views/login.html"));
})

app.post('/api/users/login', (req, res) => {
  // 1. find email in database
  User.findOne({ email: req.body.email }, (err, user) => {
    if (!user) {
      return res.json({
        loginSuccess: false,
        message: 'no matched email'
      })
    }
    // 2. if email exist in database, confirm password
    user.comparePassword(req.body.password, (err, isMatch) => {
      if (!isMatch) return res.json({ loginSuccess: false, message: 'password is not correct' })
      // 3. if pass word is matched, create token
      user.genToken((err, user) => {
        if (err) return res.status(400).send(err)

        // save token to cookie
        console.log(req);
        res.cookie('x_auth', user.token)
          .status(200)
          .redirect(`http://${req.hostname}/ClothesSeparationAPI/`);
          // .json({ loginSuccess: true, userid: user._id })
      })
    })
  })
})

// add auth middle ware
app.get('/api/users/auth', auth, (req, res)=>{
  // if this block started, auth middle ware is success

  res.status(200).json({
    _id: req.user._id,
    isAdmin: req.user.role === 0 ? false : true, // role 0 : normal user, role not 0 : admin
    isAuth: true,
    email: req.user.email,
    name: req.user.name,
    role: req.user.role,
    image: req.user.image
  })
})

// logout : delete token
app.get('/api/users/logout', auth, (req, res)=>{
  User.findOneAndUpdate({_id: req.user._id},
    {token: ''}
    , (err, user)=>{
      if(err) return res.json({ success: false, err })
      return res.status(200).send({
        success: true
      })
    })
})

app.get('/api/hello', (req,res)=>{
  res.send('hello axios!')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})