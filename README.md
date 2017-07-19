HackMIT Puzzle 2017 Workspace
=

This contains a writeup of my solutions to the HackMIT 2017 [admissions puzzles](https://delorean.codes), and most of the files and code I generated to solve them.

**The writeup is in [writeup.md](writeup.md) in this repo.** The solutions to the five problems are stored under the third-level domains on the puzzle website:

1. `warp`
2. `store`
3. `the`
4. `hotsinglebots`
5. `captcha`

License
-

**TL;DR: If I wrote it, MIT or CC-BY-4.0. If someone else wrote it or partially wrote it, whatever the original license was.**

All code in this repo, unless otherwise noted below, is Copyright &copy;&nbsp;2017 Alex Meed, and distributed under the MIT License. See [LICENSE.MIT](LICENSE.MIT).

Everything in this repo other than code, unless otherwise noted below, is either machine-generated or Copyright &copy;&nbsp;2017 Alex Meed. Those items to which I hold the copyright are distributed under the [Creative Commons 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

The following files are copies or derivatives of other people's work and have different licenses:
- These files, or portions of files, are copies or derivatives of parts of the HackMIT 2017 admissions puzzle website.

    - `warp/great_scott`
    - `warp/xxd-WarpCLI-orig`
    - `warp/WarpCLI2/javap-*`, `warp/WarpCLI2/xxd-*`, `warp/WarpCLI2/META-INF/*`
    - `hotsinglebots/model.hdf5`, `hotsinglebots/model.json`, `hotsinglebots/model.yaml`
    - `hotsinglebots/brain.py` (only the `classes` array)
    - `captcha/labels2/**`
    - `captcha/letout.png`
    - `captcha/lines.*`
    - `captcha/preprocess_test*`
- This file is a derivative of a transcription of the film *Back To The Future*:
    - `the/bttf`
- This file is a derivative of [`examples/conv_filter_visualization.py`](https://github.com/fchollet/keras/blob/master/examples/conv_filter_visualization.py) in the official Keras distribution. The following copyright notice applies to it:

        COPYRIGHT

        All contributions by François Chollet:
        Copyright (c) 2015, François Chollet.
        All rights reserved.

        All contributions by Google:
        Copyright (c) 2015, Google, Inc.
        All rights reserved.

        All contributions by Microsoft:
        Copyright (c) 2017, Microsoft, Inc.
        All rights reserved.

        All other contributions:
        Copyright (c) 2015 - 2017, the respective contributors.
        All rights reserved.

        Each contributor holds copyright over their respective contributions.
        The project versioning (Git) records all such contribution source information.

        LICENSE

        The MIT License (MIT)

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.

    - `hotsinglebots/backprop.py`
- This file portion is a derivative of [`tensorflow/examples/tutorials/mnist/mnist_softmax.py`](https://github.com/tensorflow/tensorflow/blob/r1.2/tensorflow/examples/tutorials/mnist/mnist_softmax.py) in the official TensorFlow distribution. The following copyright notice applies to it:

        # Copyright 2015 The TensorFlow Authors. All Rights Reserved.
        #
        # Licensed under the Apache License, Version 2.0 (the "License");
        # you may not use this file except in compliance with the License.
        # You may obtain a copy of the License at
        #
        #     http://www.apache.org/licenses/LICENSE-2.0
        #
        # Unless required by applicable law or agreed to in writing, software
        # distributed under the License is distributed on an "AS IS" BASIS,
        # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        # See the License for the specific language governing permissions and
        # limitations under the License.

    See [LICENSE.APACHE](LICENSE.APACHE).

    - `captcha/brain.py` (only the `model` function and parts of the `main` function)
