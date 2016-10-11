language: PYTHON
name:     "HPOlib.cv"

variable {
 name: "enterLongThresh"
 type: FLOAT
 size: 1
 min:  0.0
 max:  0.03
}

variable {
 name: "exitLongThresh"
 type: FLOAT
 size: 1
 min:  0.0
 max:  0.03
}

variable {
 name: "reversalSig"
 type: INT
 size: 1
 min:  1
 max:  5
}

