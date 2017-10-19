# Python OP_RETURN

This is a fork of the coinspark repository (https://github.com/coinspark/python-OP_RETURN) which is
distributed under the MIT license.

I have made some changes to the code to better achieve what I need to do:
 
* Added the public facing modules into a function, so they can be called from code,
but calling the function in `__main__` so should still be callable externally
* Modified the loop in `OP_RETURN_store` so that it calls `send` rather than trying to
 build up the transaction
* Added the option to send non-standard transactions by removing the check for `OP_RETURN_MAX_BYTES`
in send.  Most people probably won't want to do this, so you'll need to handle it in your code somewhere
* Calculated the transaction fee according to a specified amount of satoshis per byte.  This is quite inefficient
since it requires the transaction to be signed several times to get the correct length and signature.
* Most importantly(?!) I changed formatting from tabs to spaces, and added spaces betwen equals signs
* Added the opportunity to send transactions with multiple outputs.  This is unlikely to be useful to anyone,
but for the experiment, we needed to generate multiple transactions, but ended up having them queued in mempool.
To counter this, we split our money between various addresses on the same machine