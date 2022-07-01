# PYDI (πdi)
<style>
.x-markdown h1{text-align:center;}
.x-markdown{color:pink!important}
code {color:#f0f0f0!important}
code:hover{color:red!important;font-size:initial!important}
summary{color:white!important}
.x-markdown h2 code{font-size:initial};
</style>

Pydi follows a one instruction per line structure. Each instruction has 
two parts `command` and `argument`.

## Commmand:
Commmand itself has two parts. `Keyword` and `k-Arguments`.

eg `var@_scope:fun`
<hr>

### Keyword: 
Obligatory, Each keyword is for a specific action. 

eg `print`
<hr>

###  k-Arguments:
Non-essential,of object data structure. Skipping does not raise any errors.
Keyword and k-Arguments are separated by `@_`. For skipping it you can 
just write the keyword. But to ensure backwards compatibility it is always
recomended to add @_0 to the keyword which works same in newer versions.

eg . `r:10,f:5,jarsize:1kb,z:null`.

## Argument or arg:

Obligatory, arguments are interpreted diffrently in diffrent commands. For 
example in `print` command it is interpreted as an expression and `createDb`
treats it as name.

## DataTypes:

There are five essential data types :
<details><summary>Integer(int)</summary>Representing Integers, Written like normal using indo-arabic numerals.  eg <code>12</code>. A number may not start with <code>0</code>. Convention of naming is Camelcase <code>thisNumber</code>.</details>
<details><summary>String (str)</summary>Representing Sequence of characters, written between single-quotes follows string rules. eg <code>'astring'</code>. Convention of naming is Camelcase <code>thisString</code>.</details>
<details><summary>Float (float)</summary>Representing Decimals, Written like normal decimals eg <code>10.35</code>Convention of naming : should start with <code>.</code> eg <code>_myDecimal</code></details>
<details><summary>Boolean (bool)</summary>Representing True or False, Written as <code>True</code> or <code>False</code>. The naming Convention is to add <code>is</code> or <code>are</code> before the name. eg <code>isRunning</code>.</details>
<details><summary>Scope (sc)</summary>Scopes follow object data structure. Scopes can have Integers, Floating Point Numbers, Booleans and Strings in it.naming Convention is to write them in capilised form. eg <code>MY_OBJECT</code>.</details>

## `Var` Commmand and Similar Topics
`var` command is used to add varibles. It takes declaration type of argument i.e 

`Vartype:varName=expr`

## Declaring Scopes
You will have to add `scope:yourScope` k-arg to var command. Rest is the same.

## Errors [Vars And Similar]

###  IllegalTypeError  
It is raised due to user providing unsupported type.
###  ValueNotOfGivenTypeError  

It is raised due to user giving invalid value for the given type. eg if you
set type to `int` then give it a `string` value.
### InvalidExpressionError  

It is raised due to user providing invalid expression. 

## `Print` Command:
`print` is used to print things. It takes `expr` as argument. eg `print $$version`

## `Expression` and Similar Topics:

Expressions are composed of unit(s). Units are separated using `operators`.
Each operator performs a specific function between the two units it separates.

### Units:
Unit can be a `int`, `bool`, `str` or `float`. Either inside varible or given directly.
`InvalidExpressionError` is raised if unit is invalid.
- Acessing Varible as unit
1. From global scope. `$VarName`
2. From specific scope `myScope.myVar`
3. From super Vars `$$mySuperVar`
- Giving value directly to unit
1. `Integer(int)`/`Boolean(bool)`/`Float(float)` : Directly.
2. `String(str)` : Inside single-quotes.

### Operators:

#### `+` : Arithmetic Plus Operator. 

Valid Structure:

1. `str` + `str`  
 Cocatinates two Strings.
2. `number` + `number`  
 Adds `number` and `number`.

#### `-` : Arithmetic Minus operator.

Valid Structure:

1. `number` - `number`  
  Subtracts `number` from `number` in order.


#### `*` : Arithmetic Into Operator

Valid Structure:

1. `number` * `number`  
  Multiplies `number` and `number`.

2. `str` * `number`  or  `number` * `str`  
  Results In Repeating The Given String `number` times.

#### `/` : Arithmetic Division Operator

Valid Structure:

1. `number` / `number`  
Divides `number` from `number` in order.
Note : Returns `Float`.

#### `%` Arithmetic Modulas Operator

Valid Structure

1. `number1` % `number2`  
  Returns the remainder of `number1`/`number2`.

#### `<` Logical Less-Than Operator

Valid Structure

1. `number1` < `number2`  
  Returns Boolean value `True` If `number1` is less than `number2` else 
  `False`.

#### `>` Logical Greater-Than Operator

Valid Structure

1. `number1` > `number2`  
  Returns Boolean value `True` If `number1` is greater than `number2` else 
  `False`.

#### `~` Logical Equalence Operator

1. `str/int/float/bool` ~ `str/int/float/bool`
  Returns Boolean value `True` if both are equal else `False`.

#### `^` Logical Equalence Operator


1. `str/int/float/bool` ^ `str/int/float/bool` 
   Returns Boolean value `True` if both are unequal else `False`.

#### `|` Logical Or Operator

1. `bool` | `bool`  
   If one or two of them are `True` it Returns Boolean value `True` else 
  `False`.

#### `&` Logical And Operator

1. `bool` | `bool`   
  If both are `True` it Returns Boolean value `True` else `False`.
  Note `int` `0` and empty string `''` is parsed as `False` and rest of 
  the values are parsed as `True`.

## Functional Groups On Units

Units can have Functional Groups attached to them.
`:func:Unit`
It performs certain functions on unit eg `:int:'50'` converts string `50`
into `int` type.
### Multiple Functional Groups
 
 eg `:str::len:'MynameisYaverJavid'`
 
 `:len:` first converts `'MynameisYaverJavid'` into its length which is an 
 `int` then `:str:` converts that length into string. The one on the right 
 will used first.