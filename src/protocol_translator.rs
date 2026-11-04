//! M70: normaliza mensagens tipadas e quadros CAN clássicos.
//!
//! Não abre conexões de rede nem acessa um dispositivo CAN. O payload recebido é
//! preservado como JSON e o frame CAN é representado por seus campos estruturados.

use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "protocol", content = "message", rename_all = "snake_case")]
pub enum NetworkMessage {
    GrpcJson(Value),
    WebSocketJson(Value),
    CanBusFrame { id: u32, data: Vec<u8>, extended: bool },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct NormalizedMessage {
    pub source_protocol: String,
    pub payload: Value,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TranslationError {
    InvalidCanId(u32),
    InvalidCanLength(usize),
}

impl fmt::Display for TranslationError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidCanId(id) => write!(f, "ID CAN inválido: {id:#x}"),
            Self::InvalidCanLength(len) => write!(f, "comprimento de CAN clássico inválido: {len} bytes"),
        }
    }
}

impl std::error::Error for TranslationError {}

pub struct ProtocolTranslator;

impl ProtocolTranslator {
    pub fn translate_to_internal(input: NetworkMessage) -> Result<NormalizedMessage, TranslationError> {
        match input {
            NetworkMessage::GrpcJson(payload) => Ok(NormalizedMessage {
                source_protocol: "grpc_json".into(), payload,
            }),
            NetworkMessage::WebSocketJson(payload) => Ok(NormalizedMessage {
                source_protocol: "websocket_json".into(), payload,
            }),
            NetworkMessage::CanBusFrame { id, data, extended } => {
                let max_id = if extended { 0x1fff_ffff } else { 0x7ff };
                if id > max_id { return Err(TranslationError::InvalidCanId(id)); }
                if data.len() > 8 { return Err(TranslationError::InvalidCanLength(data.len())); }
                Ok(NormalizedMessage {
                    source_protocol: "can_bus_classic".into(),
                    payload: serde_json::json!({"id": id, "extended": extended, "data": data}),
                })
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn preserves_json_payload_and_validates_can_frame() {
        let msg = NetworkMessage::WebSocketJson(serde_json::json!({"event": "hello"}));
        let normalized = ProtocolTranslator::translate_to_internal(msg).unwrap();
        assert_eq!(normalized.payload["event"], "hello");

        let invalid = NetworkMessage::CanBusFrame { id: 0x800, data: vec![0; 8], extended: false };
        assert_eq!(ProtocolTranslator::translate_to_internal(invalid), Err(TranslationError::InvalidCanId(0x800)));
    }
}
