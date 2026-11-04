//! M60: fachada para integração com um KEM pós-quântico real.
//!
//! Este módulo NÃO implementa criptografia. Ele não deve fabricar bytes de chave,
//! ciphertext ou segredo compartilhado. Uma aplicação precisa fornecer um backend
//! revisado que implemente um algoritmo padronizado, por exemplo ML-KEM conforme
//! FIPS 203, por meio da trait abaixo.

use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct KeyPair {
    pub public_key: Vec<u8>,
    /// Material secreto: não registre nem exponha em logs. Em produção, prefira
    /// tipos de chave protegidos/zerizados fornecidos pela biblioteca criptográfica.
    pub(crate) secret_key: Vec<u8>,
}

impl KeyPair {
    pub fn from_backend_parts(public_key: Vec<u8>, secret_key: Vec<u8>) -> Self {
        Self { public_key, secret_key }
    }

    /// Indica apenas o comprimento armazenado; não devolve o segredo.
    pub fn secret_key_len(&self) -> usize {
        self.secret_key.len()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Encapsulation {
    pub ciphertext: Vec<u8>,
    pub shared_secret: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CryptoError(pub String);

impl fmt::Display for CryptoError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for CryptoError {}

/// Implementado por um provedor criptográfico real e revisado.
/// O contrato exige aleatoriedade criptograficamente segura e validação de entradas.
pub trait KemBackend {
    fn algorithm(&self) -> &'static str;
    fn generate_keypair(&self) -> Result<KeyPair, CryptoError>;
    fn encapsulate(&self, public_key: &[u8]) -> Result<Encapsulation, CryptoError>;
    fn decapsulate(&self, keypair: &KeyPair, ciphertext: &[u8]) -> Result<Vec<u8>, CryptoError>;
}

pub struct PostQuantumEngine<B> {
    backend: B,
}

impl<B: KemBackend> PostQuantumEngine<B> {
    pub fn new(backend: B) -> Self {
        Self { backend }
    }

    pub fn algorithm(&self) -> &'static str {
        self.backend.algorithm()
    }

    pub fn generate_keypair(&self) -> Result<KeyPair, CryptoError> {
        self.backend.generate_keypair()
    }

    pub fn encapsulate(&self, public_key: &[u8]) -> Result<Encapsulation, CryptoError> {
        self.backend.encapsulate(public_key)
    }

    pub fn decapsulate(&self, keypair: &KeyPair, ciphertext: &[u8]) -> Result<Vec<u8>, CryptoError> {
        self.backend.decapsulate(keypair, ciphertext)
    }
}
