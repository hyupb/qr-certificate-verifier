# 조사 노트

## 1. 핵심 개념

 DID : 개인이 스스로 소유하는 탈중앙 식별자. 중앙 기관 계정이 아니라 본인 소유의 ID | 소지자의 공개키를 ID처럼 사용 (단순화) 
 VC (Verifiable Credential) : 발급자가 서명해서 내려준 증명서 원본. "이름·생년월일·거주지"를 담은 서명된 문서 | `credentials` 테이블의 증명서 한 건 
 VP (Verifiable Presentation) : 소지자가 검증자에게 제출하는, VC 중 일부만 골라 담고 자기 서명을 더한 제출물 | 검증 요청에 대한 응답 (선택 공개 + nonce 서명) 

## 2. 실제 방식과 내 구현의 차이

| 항목           | 실제 모바일 신분증             | 내 구현 (단순화)                                    |
|----------------|-------------------------------|----------------------------------------------------|
| 키 저장 위치   | 폰 보안 영역(TEE/eSE)          | 서버 DB (실습용, 프로덕션엔 부적합함을 README에 명시) |
| 신원 공유 방식 | 블록체인 기반 DID 등록          | 발급자 공개키를 파일로 배포 (발급자 단일 신뢰)       |
| 전달 방식      | QR 촬영 / BLE / NFC            | QR 코드 1가지만 구현                                |
| 선택적 공개    | 항목별 암호화·해시 후 부분 공개 | 항목별 salted hash로 단순화                          |

## 3. ERD

\`\`\`mermaid
erDiagram
    CREDENTIALS ||--o{ REVOCATIONS : "폐기될 수 있음"
    CREDENTIALS ||--o{ VERIFY_REQUESTS : "검증 요청 대상"
    VERIFY_REQUESTS ||--o{ AUDIT_LOGS : "기록됨"

    CREDENTIALS {
        string id PK
        string holder_pubkey
        string issuer_id
        json claims_hash
        datetime issued_at
        datetime expires_at
        string signature
    }

    REVOCATIONS {
        string credential_id PK
        datetime revoked_at
        string reason
    }

    VERIFY_REQUESTS {
        string id PK
        string nonce
        json requested_fields
        datetime created_at
        datetime expires_at
        boolean used
    }

    AUDIT_LOGS {
        string id PK
        string actor
        string action
        string target_id
        datetime created_at
    }
\`\`\`