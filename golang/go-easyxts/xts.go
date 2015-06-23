package xts

import "golang.org/x/crypto/xts"
import "crypto/aes"
import "crypto/rand"
import "fmt"
import "errors"

type XTSDevice struct {
	key            []byte
	sectorSize     uint64
	sectorTotal    uint64
	lastUsedSector uint64
	cipher         *xts.Cipher
}

//Creates a new XTS Device
//All values can be nil or 0, they will be initialized to:
//key := a random new one
//sectorSize := 16 (need a multiple of 16)
//sectorTotal := 3 (at least 3 blocks are needed for this ciphertext stealing implementation)
func NewDevice(key []byte, sectorSize uint64, sectorTotal uint64) (x *XTSDevice, err error) {
	if key == nil {
		key := make([]byte, 32)
		_, err := rand.Read(key)
		if err != nil {
			return nil, err
		}
	} else {
		if len(key) != 32 && len(key) != 64 {
			err := errors.New(fmt.Sprintf("Key is expected to have length 32 or 64, got %d", len(key)))
			return nil, err
		}
	}
	if sectorSize == 0 {
		sectorSize = 16
	} else if sectorSize%16 != 0 {
		return nil, errors.New(fmt.Sprintf("Sector size is expected to be a multiple of 16, got %d", sectorSize))
	}

	if sectorSize < 3 {
		sectorSize = 3
	}

	x = &XTSDevice{
		key:            key,
		sectorSize:     sectorSize,
		sectorTotal:    sectorTotal,
		lastUsedSector: 0,
	}
	if x.cipher, err = xts.NewCipher(aes.NewCipher, key); err != nil {
		return nil, err
	}
	return x, nil
}

//For now, plaintext length needs to be equal to sector size
func (x *XTSDevice) Encrypt(plaintext []byte, sector uint64) (ciphertext []byte, err error) {
	if plaintext == nil || sector < 0 {
		return nil, errors.New("Invalid parameters. Plaintext can't be nil and sector can't be less than 0")
	}
	ciphertext = make([]byte, x.sectorSize)
	x.cipher.Encrypt(ciphertext, plaintext, sector)
	return ciphertext, nil
}

//For now, ciphertext length needs to be equal to sector size
func (x *XTSDevice) Decrypt(ciphertext []byte, sector uint64) (plaintext []byte, err error) {
	if ciphertext == nil || sector < 0 {
		return nil, errors.New("Invalid parameters. Ciphertext can't be nil and sector can't be less than 0")
	}
	plaintext = make([]byte, x.sectorSize)
	x.cipher.Decrypt(plaintext, ciphertext, sector)
	return plaintext, nil
}
