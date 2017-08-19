# HookRace Jr.
In this project you will be building your own 2D game that will read user input, display graphics, and simulate 2D physics!

### Prerequisites (Ubuntu 16.04)

* Python 3.5
* Install SDL2, SDL2_image, SDL2_ttf via `apt`:
    ```bash
    sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
    ```
* Install pysdl2 via `pip3`:
    ```bash
    pip3 install --user pysdl2
    ```

> Optional: `mypy`

### Objectives 

1. The Window (game.py)
2. The Renderer and Game Loop (game.py)
3. The Game State and Update Method (game.py)
4. Render Player Texture (player.py)
5. Physics (player.py)
6. Collision Detection and AABB (tilemap.py)
7. Camera (game.py)
8. Stopwatch (stopwatch.py)

#### Givens

Textbox, Point2d, Vector2d, Controller, Stopwatch

## Your Challenge
Follow the steps in each objective to complete your game. You may customize your game to your liking after completing each objective. 

### Objective 1: The Window

New Programming Concepts:

* Tuples
* Classes 
* Keyword Arguments
* Module Variables
* Local Variables
* Method (aka. Member Functions)

**Steps:**

1. Choose a title for the window, store it as a string in a module variable
2. Choose a size for the window, store it as a tuple of two integers in a module variable
3. Instantiate a `Window` object, passing the title as the first argument,
   and the size as a named argument with name `size`, and...
4. Store the created `Window` instance in a `window` variable in the `main` function
5. Call the `show` method on the `Window` object

Documentation for `Window`:

* https://pysdl2.readthedocs.io/en/rel_0_9_5/modules/sdl2ext_window.html

Resources:<br>
Classes in Python Practice - https://www.learnpython.org/en/Classes_and_Objects<br>
Sharing variables across files - http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm

### Objective 2: The Renderer

New Programming Concepts:

* Properties
* RGB colors
* `while` loop 
* `break` statement

**Steps:**

1. Instantiate a `Renderer` object, passing the window from Objective 1 as its only argument, and...
2. Store the created `Renderer` instance in a `renderer` variable in the `main` method
3. Instantiate a `Color` object with three keyword arguments (`r`, `g`, and `b`), store it in a local variable in the `main` function
4. Assign the created color to the `color` property on the `Renderer` object 
5. Inside the game loop, call the `clear` and `present` methods on the `Renderer` object

> I used red = 110, green = 132, blue = 174

Documentation for `Renderer` and `Color`:

* https://pysdl2.readthedocs.io/en/rel_0_9_5/modules/sdl2ext_sprite.html
* https://pysdl2.readthedocs.io/en/rel_0_9_5/modules/sdl2ext_color.html

Questions:

* When does the game loop exit?

Resources:<br>
While Loops in Python - https://pythonschool.net/basics/while-loops/

### Objective 3: The Game Loop

New Game Concepts:

* Game Loop
* Frame 
* Time Step

**Steps:**

1. Instantiate a `Game` object, passing the `Resources` object as the only argument
2. In between the `clear` and `present` calls to the `Renderer` object, call the `render` method on the `Game` object. Pass it the appropriate arguments.
3. Before the rendering, call the `update` method the appropriate number of frames.

For step 3. you need to use a `while`-loop, the local `lag` variable, and the `SECONDS_PER_UPDATE` module variable.

The `lag` variable represents the amount of time in seconds that has yet to be updated. Each time we process a frame, the lag should be decreased by the amount of time that frame represents (i.e. the `SECONDS_PER_UPDATE`).

> Hint: modify the `lag` variable each time though the loop as appropriate, and use it to check for the finished condition

Additional Reading:

http://gameprogrammingpatterns.com/game-loop.html

### Objective 4: Render Player Texture

New Programming Concepts:

* Unpacking a Tuple
* `for` loop
* Modules
* `import`
* Member variable

New Graphics Concepts:

* Point
* Vector
* Sprite Sheet

**Steps:**

1. Find the correct coordinates for the player texture to be drawn
2. Read the explanation on what is happening to the sprite sheet
3. Use the `renderer.copy` method to draw each part of the player texture in the correct place
4. Import the player module into the game module
5. Create a Player member variable on the Game object called `player` (make sure to pass it the Resources)
6. Call the render method on the game's player object during the game's render method (make sure to pass it the camera)

For step 1, consider the following diagram:

```
            |--1--2--3--4--| <-- x-axis screen (int)
            |     *        | <-- player
0--1--2--3--|--5--6--7--8--| <-- x-axis world (float)
            ^                <-- camera
```

For step 2, read:

We need to cut up the player sheet into an array of tuples.
The upper left is (0, 0). The total size is 256x128.

If you divide the sections into 32x32 squares it looks like:

```
|a a a|b b b|-|-|  a = body
|a a a|b b b|c c|  b = body shadow
|a a a|b b b|d d|  c = foot
|   |e|-|-|-|-|-|  d = foot shadow
                   e = basic eye (left)
``` 
We take the pieces and overlay them on top of each other:
```
                          ( dx,  dy,   w,  h)
1. foot shadow (back)  -> (-60,   0,  96, 48) <-- 3/2 scale
2. foot (back)         -> (-60,   0,  96, 48) <-- 3/2 scale
3. body shadow         -> (-48, -48,  96, 96)
4. body                -> (-48, -48,  96, 96)
5. foot shadow (front) -> (-36,   0,  96, 48) <-- 3/2 scale
6. foot (front)        -> (-36,   0,  96, 48) <-- 3/2 scale
7. basic eye (left)    -> (-18, -21,  36, 36) <-- 9/8 scale
8. basic eye (right)   -> ( -6, -21,  36, 36) <-- 9/8 scale *FLIPPED*
```


For step 3. you will be given the sprite sheet mappings that split it up like a puzzle and rebuild it using `render.copy`.
The parameters are the `texture` followed by the unpacked tuple variables:
1. source - the x, y, w, h of the texture puzzle piece to "cut out"
2. destination - the x, y, w, h of where to draw it on screen
3. flipped - whether to flip the image and how (i.e. vert/hort)

The flipped parameter is a keyword argument named `flip`. 

Use a for loop to iterate over and unpack the body parts.

> Bonus: Feel free to tweak the mappings from step 2. and see what happens :)

> Bonus: Get a different player texture here: https://ddnet.tw/skins/

### Objective 5: The Tilemap

New Programming Concepts:
* Reading a File

**Steps:**

1. Get the path of the tilemap file from the Resources object
2. Open the file of the tilemap file for reading
3. Read through each line
4. For each line split it into the numbers (requires conversion from string to int)
5. Store each number in the tiles array
6. Along the way keep track of the width and height of the tilemap
   (i.e. each line adds to the height, the number of numbers in a line is the width)
7. Read the lookup function for transforming world locations into tiles
8. Convert from the two dimensional (nx, ny) = (col, row) values back into tiles index for tile lookup
9. import, create, and add a Tilemap to the Game object

> Bonus: verify that the width is the same in each line/row of the tilemap


### Objective 6: The Update Method

New Game Concepts:

* The Update Method
* Physics Engine
* Collision Detection

**Steps:**

1. Call the player update method from the game update method
2. Use the tilemap to move the player by the new velocity determined by the physics logic

Our physics engine is going to have the following traits:
* gravity (constant acceleration)
* horizontal friction
* terminal horizontal velocity
* acceleration-based running 
* velocity-based jumping

The physics engine is what determines the feel of the character movement.

Here how ours determines the velocity to apply to the player:

1. If user wants to jump (and we are on the ground) vertical velocity is set to 21 pixels / frame
2. Gravity is applied every frame to decrease velocity by a 0.75 pixels / frame
3. If we are on the ground, the horizontal velocity slows to a half of what it was
4. Otherwise, the horizontal velocity shows to 95% of what it was 
5. If we are on the ground and the user is moving the horizontal velocity is increased by 4 pixels / frame in that direction
6. If we are in the air and the user is moving the horizontal velocity is increased by 2 pixels / frame in that direction
7. The horizonal velocity is capped at 8 pixels / frame

Completing step 2 then does:

8. Modify the player position by the new velocity vector
9. If any movement along our velocity vector would move us into a solid tile our velocity drops to 0 in that direction, and we move up to the edge of the solid tile in the direction of the vector.

> Bonus: Play with the physics engine components and see what happens

> Bonus: Try modifying the `UPDATES_PER_SECOND` variable and see what happens

Additional Reading:

http://gameprogrammingpatterns.com/update-method.html

### Objective 7: Camera

Set up camera movement to follow the player.

**Steps:**
* Find the Objective 7 markers in the code and follow directions


### Objective 8: Stopwatch

Augment the `Game` update method.

1. Get the tile type from the tile map for the player position
2. If the tile type is a start tile, then call start on the stopwatch
3. If the tile type is an end tile, then call stop on the stopwatch
4. Otherwise, just call step on the stopwatch


### What next?

* Build your own map?
* Play with the physics engine
* Change player skin
* Add a second player... can they race?
* Double Jump?

### Based on:

https://pysdl2.readthedocs.io/en/rel_0_9_5/

https://hookrace.net/blog/writing-a-2d-platform-game-in-nim-with-sdl2/

