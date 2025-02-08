import styled from 'styled-components';
import { FormContainer } from './styles/FormContainer';
import { FormInput } from './styles/FormInput';
import { FormSelect } from './styles/FormSelect';
import { SubmitButton } from './styles/SubmitButton';
import { countries } from '../data/countries';
import { cities } from '../data/cities';
import { universities } from '../data/universities';
import { phoneCodes } from '../data/phoneCodes';
import { sdgs } from '../data/sdgs';

const FormWrapper = styled.div`
  max-width: 960px;
  margin: 0 0 25px;
  border: 1.6px solid rgb(166, 166, 166);
  padding: 0 45px 45px;
  border-radius: 15px;
`;

const FormTitle = styled.h2`
  font-size: 32px;
  margin-bottom: 40px;
`;

const FormLabel = styled.label`
  font-weight: 600;
  margin-top: 15px;
  margin-bottom: 5px;
  display: block;
`;

const FormHint = styled.span`
  font-style: italic;
  padding: 0 0 5px 0;
  display: block;
`;

const TeamMemberTitle = styled.h3`
  margin-block: 0;
  font-weight: bold;
`;

const TeamMemberSubtitle = styled.p`
  margin-block-start: 0;
  font-weight: bold;
`;

const TeamMemberHint = styled.p`
  margin-block-end: 0;
  font-style: italic;
`;

const CheckboxContainer = styled.div`
  width: 100%;
  margin: 15px 0;
  position: relative;
  display: flex;
  flex-direction: column;
`;

const CheckboxLabel = styled.label`
  position: relative;
  min-height: 27px;
  display: block;
  padding-left: 30px;
  margin-bottom: 0;
  font-weight: 400;
  cursor: pointer;
`;

const RegistrationForm = () => {
  return (
    <FormWrapper>
      <FormTitle>The 2025 competitor registration form is now open!</FormTitle>
      
      <FormContainer>
        {/* Startup Information */}
        <FormLabel htmlFor="startupName">Startup Name *</FormLabel>
        <FormHint>Hult Prize will recognize this as the team name</FormHint>
        <FormInput 
          id="startupName"
          name="Startup_Name__c"
          required
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="country">Country *</FormLabel>
        <FormHint>Where the university you're representing is located</FormHint>
        <FormSelect
          id="country" 
          name="country_code"
          required
        >
          <option value="">Country...</option>
          {countries.map(country => (
            <option key={country.value} value={country.value}>
              {country.label}
            </option>
          ))}
        </FormSelect>

        <FormLabel htmlFor="city">City *</FormLabel>
        <FormSelect
          id="city"
          name="city"
          required
          style={{ borderColor: 'rgb(230, 0, 127)' }}
        >
          <option value="">City...</option>
          {cities.map(city => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
        </FormSelect>

        <FormLabel htmlFor="university">University *</FormLabel>
        <FormHint>If you do not see your university listed, scroll to the bottom and select "other"</FormHint>
        <FormSelect
          id="university"
          name="UniversityId__c"
          required
        >
          <option value="">University...</option>
          {universities.map(university => (
            <option key={university.value} value={university.value}>
              {university.label}
            </option>
          ))}
        </FormSelect>

        {/* Team Captain Information */}
        <TeamMemberTitle>Team Member Information:</TeamMemberTitle>
        <ol>
          <li>
            <TeamMemberSubtitle>Team Captain Information</TeamMemberSubtitle>
            <TeamMemberHint>The team captain will be the main point of contact with Hult Prize</TeamMemberHint>
          </li>
        </ol>

        <FormLabel htmlFor="firstName">First Name *</FormLabel>
        <FormInput
          id="firstName"
          name="FirstName"
          type="text"
          required
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="lastName">Last Name *</FormLabel>
        <FormInput
          id="lastName"
          name="LastName"
          type="text"
          required
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="email">Email *</FormLabel>
        <FormInput
          id="email"
          name="Email"
          type="email"
          required
          pattern="^[\p{L}/gu0-9.!#$%&+'^_`{}~-]+@[\p{L}/gu0-9-]+[.]+(?:.[\p{L}/gu0-9-]+)*$"
        />

        <FormLabel htmlFor="phone">Phone *</FormLabel>
        <FormHint>Do not include any country codes, symbols, or spaces</FormHint>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '15px',
          margin: '0',
        }}>
          <FormSelect
            id="phoneCode"
            required
            style={{ width: '54%' }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map(code => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone"
            type="tel"
            pattern="[0-9.]+"
            required
            style={{ marginTop: '15px' }}
          />
          <input type="hidden" name="Phone" required />
        </div>

        <FormLabel htmlFor="differentUniversity">Is this member of your team from a different University?</FormLabel>
        <FormHint>All members can be from a different university</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="differentUniversity"
            name="Is_a_member_different_University__c"
            value="true"
            required
          />
          <CheckboxLabel htmlFor="differentUniversity">
            <span>Yes</span>
          </CheckboxLabel>
        </CheckboxContainer>

        {/* Team Member 2 */}
        <TeamMemberSubtitle>Team Member 2</TeamMemberSubtitle>
        
        <FormLabel htmlFor="firstName2">First Name *</FormLabel>
        <FormInput
          id="firstName2"
          name="First_Name_TM2__c"
          type="text"
          required
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="lastName2">Last Name *</FormLabel>
        <FormInput
          id="lastName2"
          name="Last_Name_TM2__c"
          type="text"
          required
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="email2">Email *</FormLabel>
        <FormInput
          id="email2"
          name="Email_TM2__c"
          type="email"
          required
          pattern="^[\p{L}/gu0-9.!#$%&+'^_`{}~-]+@[\p{L}/gu0-9-]+[.]+(?:.[\p{L}/gu0-9-]+)*$"
        />

        <FormLabel htmlFor="phone2">Phone *</FormLabel>
        <FormHint>Do not include any country codes, symbols, or spaces</FormHint>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '15px',
          margin: '0',
        }}>
          <FormSelect
            id="phoneCode2"
            required
            style={{ width: '54%', marginRight: '15px' }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map(code => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone2"
            type="tel"
            pattern="[0-9.]+"
            required
            style={{ marginTop: '15px' }}
          />
          <input type="hidden" name="Phone_TM2__c" required />
        </div>

        <FormLabel htmlFor="differentUniversity2">
          Is this member of your team from a different University?
        </FormLabel>
        <FormHint>All members can be from a different university.</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="differentUniversity2"
            name="Is_a_member_different_UniversityTwo"
            value="true"
            required
          />
          <CheckboxLabel htmlFor="differentUniversity2">
            <span>Yes</span>
          </CheckboxLabel>
        </CheckboxContainer>

        {/* Team Member 3 */}
        <TeamMemberSubtitle>Team Member 3</TeamMemberSubtitle>
        
        <FormLabel htmlFor="firstName3">First Name</FormLabel>
        <FormInput
          id="firstName3"
          name="First_Name_TM3__c"
          type="text"
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="lastName3">Last Name</FormLabel>
        <FormInput
          id="lastName3"
          name="Last_Name_TM3__c"
          type="text"
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="email3">Email</FormLabel>
        <FormInput
          id="email3"
          name="Email_TM3__c"
          type="email"
          pattern="^[\p{L}/gu0-9.!#$%&+'^_`{}~-]+@[\p{L}/gu0-9-]+[.]+(?:.[\p{L}/gu0-9-]+)*$"
        />

        <FormLabel htmlFor="phone3">Phone</FormLabel>
        <FormHint>Do not include any country codes, symbols, or spaces</FormHint>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '15px',
          margin: '0',
        }}>
          <FormSelect
            id="phoneCode3"
            style={{ width: '54%', marginRight: '15px' }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map(code => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone3"
            type="tel"
            pattern="[0-9.]+"
            style={{ marginTop: '15px' }}
          />
          <input type="hidden" name="Phone_TM3__c" />
        </div>

        <FormLabel htmlFor="differentUniversity3">
          Is this member of your team from a different University?
        </FormLabel>
        <FormHint>All members can be from a different university.</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="differentUniversity3"
            name="Is_a_member_different_UniversityThree"
            value="true"
            required
          />
          <CheckboxLabel htmlFor="differentUniversity3">
            <span>Yes</span>
          </CheckboxLabel>
        </CheckboxContainer>

        {/* Team Member 4 */}
        <TeamMemberSubtitle>Team Member 4</TeamMemberSubtitle>
        
        <FormLabel htmlFor="firstName4">First Name</FormLabel>
        <FormInput
          id="firstName4"
          name="First_Name_TM4__c"
          type="text"
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="lastName4">Last Name</FormLabel>
        <FormInput
          id="lastName4"
          name="Last_Name_TM4__c"
          type="text"
          pattern="^[^()><{}~;]*$"
        />

        <FormLabel htmlFor="email4">Email</FormLabel>
        <FormInput
          id="email4"
          name="Email_TM4__c"
          type="email"
          pattern="^[\p{L}/gu0-9.!#$%&+'^_`{}~-]+@[\p{L}/gu0-9-]+[.]+(?:.[\p{L}/gu0-9-]+)*$"
        />

        <FormLabel htmlFor="phone4">Phone</FormLabel>
        <FormHint>Do not include any country codes, symbols, or spaces</FormHint>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '15px',
          margin: '0',
        }}>
          <FormSelect
            id="phoneCode4"
            style={{ width: '54%', marginRight: '15px' }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map(code => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone4"
            type="tel"
            pattern="[0-9.]+"
            style={{ marginTop: '15px' }}
          />
          <input type="hidden" name="Phone_TM4__c" />
        </div>

        <FormLabel htmlFor="differentUniversity4">
          Is this member of your team from a different University?
        </FormLabel>
        <FormHint>All members can be from a different university.</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="differentUniversity4"
            name="Is_a_member_different_UniversityFour"
            value="true"
          />
          <CheckboxLabel htmlFor="differentUniversity4">
            <span>Yes</span>
          </CheckboxLabel>
        </CheckboxContainer>

        <FormLabel htmlFor="country4">Country</FormLabel>
        <FormHint>Where your university is located</FormHint>
        <FormSelect
          id="country4"
          name="country_codeteamfour"
        >
          <option value="">Country...</option>
          {countries.map(country => (
            <option key={country.value} value={country.value}>
              {country.label}
            </option>
          ))}
        </FormSelect>

        <FormLabel htmlFor="city4">City</FormLabel>
        <FormHint>Where your university is located</FormHint>
        <FormSelect
          id="city4"
          name="city_teamfour"
        >
          <option value="">City...</option>
          {cities.map(city => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
        </FormSelect>

        <FormLabel htmlFor="university4">University</FormLabel>
        <FormHint>If you do not see your university listed, scroll to the bottom and select "other"</FormHint>
        <FormSelect
          id="university4"
          name="UniversityId_TM4__c"
        >
          <option value="">University...</option>
          {universities.map(university => (
            <option key={university.value} value={university.value}>
              {university.label}
            </option>
          ))}
        </FormSelect>

        <FormLabel htmlFor="sdg">Sustainable Development Goal (SDG) *</FormLabel>
        <FormHint>Select the main Sustainable Development Goal (SDG) your startup will align with</FormHint>
        <FormSelect
          id="sdg"
          name="Sustainable_Development_Goals__c"
          required
        >
          <option value="">Sustainable Development Goal (SDG)...</option>
          {sdgs.map(sdg => (
            <option key={sdg.value} value={sdg.value}>
              {sdg.label}
            </option>
          ))}
        </FormSelect>

        {/* Previous Experience Checkboxes */}
        <FormLabel htmlFor="experience">Previous Hult Prize experience *</FormLabel>
        <FormHint>Check all that apply</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="competitor"
            name="HP_History__c"
            value="Competitor"
            required
          />
          <CheckboxLabel htmlFor="competitor">
            <span>Competitor</span>
          </CheckboxLabel>

          <input
            type="checkbox"
            id="volunteer"
            name="HP_History__c"
            value="Global Event Volunteer"
            required
          />
          <CheckboxLabel htmlFor="volunteer">
            <span>Global Event Volunteer</span>
          </CheckboxLabel>

          <input
            type="checkbox"
            id="firstTime"
            name="HP_History__c"
            value="First Time Hearing About HP"
            required
          />
          <CheckboxLabel htmlFor="firstTime">
            <span>First Time Hearing About HP</span>
          </CheckboxLabel>

          <input
            type="checkbox"
            id="onCampus"
            name="HP_History__c"
            value="OnCampus Program Volunteer"
            required
          />
          <CheckboxLabel htmlFor="onCampus">
            <span>OnCampus Program Volunteer</span>
          </CheckboxLabel>
        </CheckboxContainer>

        <SubmitButton type="submit">Apply Now!</SubmitButton>
      </FormContainer>
    </FormWrapper>
  );
};

export default RegistrationForm; 