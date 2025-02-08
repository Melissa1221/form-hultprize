import styled from 'styled-components';

export const CheckboxContainer = styled.div`
  width: 100%;
  margin: 15px auto;
  position: relative;
  display: flex;
  flex-direction: column;
`;

export const CheckboxInput = styled.input`
  width: auto;
  opacity: 0.00000001;
  position: absolute;
  left: 0;
  margin-left: -20px;
`;

export const CheckboxLabel = styled.label`
  position: relative;
  min-height: 27px;
  display: block;
  padding-left: 30px;
  margin-bottom: 0;
  font-weight: 400;
  cursor: pointer;
`; 