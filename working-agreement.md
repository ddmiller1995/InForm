## Implementation Working Agreement

### GitHub

#### Branching
- `master` branch will act as Prod
- `dev` branch will act as a staging area
	- all feature work must be merged to `dev` before `master`
	- `dev` branch must be fully integrated and tested before merged to `master`
- All feature work will be coded up and tested on our individual branches, following the naming convention `dev-author`
 
#### Code Review
- Only pushed working, tested code
	- <em>Keep our branches clean!</em>
- Create a Pull Request to `dev` for all completed and tested feature work
- Pull Requests must be reviewed by at least one team member other than the author
	- All comments/concerns left by the reviewer must be addressed/mitigated by the author before the Pull Request can be merged

### Testing
- <b><em>Test all the code!</em></b>
- Use [`mocha`](https://www.npmjs.com/package/mocha) to test Javascript code
- Whenever you fix a bug, write a regression test. A bug fixed without a regression test is almost certainly going to break again in the future.

### React
- Follow the [React](https://facebook.github.io/react/docs/react-api.html) style guide

## Styleguide

### File Names
`all-lower-case-with-dashes.js`

### Javascript

```javascript
"use strict"; 

// use camelCase when naming objects, functions, and instances
var camelCaseVariables = "always user var"; // and always use semi-colons

// use PascalCase only when naming constructors or classes
class User {
	constructor(options) {
		this.name = options.name;
	}
}

// capitalize acronyms
var capitalizeAcronymns = "HTMLEscapeCharacters and HTTPSServer";

// place 1 space before the leading brace 
function spaceBeforeLeadingBrace() {
	console.log("test");
}

// place 1 space before the opening parenthesis in control statements
if (spaceBetweenOpeningParens) {
	jobWellDone();
}

// no space between argument list and the function name
function noSpaceBetweenFunctionAndArguments() {...}

// no more than a single space between any two lines
fruits.map({
	endingBracketsOnSeparateLines: "use double quotes"
});

var limitMethodLengthTo20Lines = function(space, after, commas) {
	var andLimitTabDepthToFiveTabs;
};

// use expressive variable names...
var goodVariableNames = [
	"successReturnToOrRedirect",
	"onTaskDescriptionChange",
];

// ...and method headers
calculateRadioFrequency() {}

// use the literal syntax for object creation
var obj = {};
var array = [];

```

### CSS
```cs
.all-lower-case-with-dashes {
}
```

### Miscellaneous

- No `console.log()` statements in master or any Prod code
- Limit line length to 100 characters
- Use tabs & always use the correct indentation
- Use a single space after the comment token 
	- // comment