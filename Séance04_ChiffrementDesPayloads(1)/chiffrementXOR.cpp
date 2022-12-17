char * Xor(char * in, int inSize, char * key, int keySize, char * out) {
	int it_key = 0;

    for (int i=0; i<inSize; i++) {
        out[i] = in[i] ^ key[it_key];
        it_key = (i + 1) % keySize;
    }
    
	return out;
}