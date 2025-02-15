import styled from "styled-components";
import { FormContainer } from "./styles/FormContainer";
import { FormInput } from "./styles/FormInput";
import { FormSelect } from "./styles/FormSelect";
import { SubmitButton } from "./styles/SubmitButton";
import { countries } from "../data/countries";
import { cities } from "../data/cities";
import { universities } from "../data/universities";
import { phoneCodes } from "../data/phoneCodes";
import { sdgs } from "../data/sdgs";
import { useState } from "react";

const FormWrapper = styled.div`
  max-width: 960px;
  margin: 0 0 25px;
  border: 1.6px solid rgb(166, 166, 166);
  padding: 0 45px 45px;
  border-radius: 15px;
  text-align: left;

  * {
    text-align: left;
  }
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
  gap: 10px;

  div {
    display: flex;
    align-items: center;

    input {
      margin-right: 10px;
    }

    span {
      margin-left: 5px;
    }
  }
`;

const RegistrationForm = () => {
  // Main form states
  const [selectedMainUniversity, setSelectedMainUniversity] = useState("");
  const [otherMainUniversity, setOtherMainUniversity] = useState("");
  const [selectedMainCity, setSelectedMainCity] = useState("");
  const [otherMainCity, setOtherMainCity] = useState("");

  // Team Captain states (for different university checkbox)
  const [selectedUniversity1, setSelectedUniversity1] = useState("");
  const [otherUniversity1, setOtherUniversity1] = useState("");
  const [selectedCity1, setSelectedCity1] = useState("");
  const [otherCity1, setOtherCity1] = useState("");
  const [isDifferentUniversity1, setIsDifferentUniversity1] = useState(false);
  const [selectedCountry1, setSelectedCountry1] = useState("");

  // Team Member 2 states
  const [selectedUniversity2, setSelectedUniversity2] = useState("");
  const [otherUniversity2, setOtherUniversity2] = useState("");
  const [selectedCity2, setSelectedCity2] = useState("");
  const [otherCity2, setOtherCity2] = useState("");
  const [isDifferentUniversity2, setIsDifferentUniversity2] = useState(false);

  // Team Member 3 states
  const [selectedUniversity3, setSelectedUniversity3] = useState("");
  const [otherUniversity3, setOtherUniversity3] = useState("");
  const [selectedCity3, setSelectedCity3] = useState("");
  const [otherCity3, setOtherCity3] = useState("");
  const [isDifferentUniversity3, setIsDifferentUniversity3] = useState(false);

  // Team Member 4 states
  const [selectedUniversity4, setSelectedUniversity4] = useState("");
  const [otherUniversity4, setOtherUniversity4] = useState("");
  const [selectedCity4, setSelectedCity4] = useState("");
  const [otherCity4, setOtherCity4] = useState("");
  const [isDifferentUniversity4, setIsDifferentUniversity4] = useState(false);

  const handleUniversityChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    setUniversity: (value: string) => void,
    setOtherUniv: (value: string) => void
  ) => {
    const value = e.target.value;
    setUniversity(value);
    if (value !== "Other") {
      setOtherUniv("");
    }
  };

  const handleCityChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    setCity: (value: string) => void,
    setOtherCityValue: (value: string) => void
  ) => {
    const value = e.target.value;
    setCity(value);
    if (value !== "Other") {
      setOtherCityValue("");
    }
  };

  const handleSelectChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    handler: (
      e: React.ChangeEvent<HTMLSelectElement>,
      setStateValue: (value: string) => void,
      setOtherValue: (value: string) => void
    ) => void,
    setStateValue: (value: string) => void,
    setOtherValue: (value: string) => void
  ) => {
    handler(e, setStateValue, setOtherValue);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validación para miembro 1
    if (isDifferentUniversity1) {
      if (!selectedCountry1 || !selectedCity1 || !selectedUniversity1) {
        alert(
          "Please fill all required fields for Team Captain's different university"
        );
        return;
      }
    }

    try {
      // Get university name instead of ID
      const universitySelect = document.getElementById(
        "university"
      ) as HTMLSelectElement;
      const universityName =
        universitySelect.options[universitySelect.selectedIndex].text;

      const formData = {
        startupName: (
          document.getElementById("startupName") as HTMLInputElement
        ).value,
        country: (document.getElementById("country") as HTMLSelectElement)
          .value,
        city: selectedMainCity === "Other" ? otherMainCity : selectedMainCity,
        university:
          selectedMainUniversity === "Other"
            ? otherMainUniversity
            : universityName,
        sdg: (document.getElementById("sdg") as HTMLSelectElement).value,
        hpHistory: Array.from(
          document.querySelectorAll('input[name="HP_History__c"]:checked')
        ).map((el) => (el as HTMLInputElement).value),
        leadSource: (
          document.querySelector(
            'input[name="LeadSource"]:checked'
          ) as HTMLInputElement
        )?.value,
        teamMembers: [
          {
            type: "captain",
            firstName: (
              document.getElementById("firstName") as HTMLInputElement
            ).value,
            lastName: (document.getElementById("lastName") as HTMLInputElement)
              .value,
            email: (document.getElementById("email") as HTMLInputElement).value,
            phone: (document.getElementById("phone") as HTMLInputElement).value,
            country: isDifferentUniversity1
              ? (document.getElementById("memberCountry1") as HTMLSelectElement)
                  .value
              : (document.getElementById("country") as HTMLSelectElement).value,
            city: isDifferentUniversity1
              ? selectedCity1 === "Other"
                ? otherCity1
                : selectedCity1
              : selectedMainCity === "Other"
              ? otherMainCity
              : selectedMainCity,
            university: isDifferentUniversity1
              ? selectedUniversity1 === "Other"
                ? otherUniversity1
                : (
                    document.getElementById(
                      "memberUniversity1"
                    ) as HTMLSelectElement
                  ).options[
                    (
                      document.getElementById(
                        "memberUniversity1"
                      ) as HTMLSelectElement
                    ).selectedIndex
                  ].text
              : selectedMainUniversity === "Other"
              ? otherMainUniversity
              : universityName,
            isDifferentUniversity: isDifferentUniversity1,
          },
          // Team Member 2
          {
            type: "member2",
            firstName: (
              document.getElementById("firstName2") as HTMLInputElement
            ).value,
            lastName: (document.getElementById("lastName2") as HTMLInputElement)
              .value,
            email: (document.getElementById("email2") as HTMLInputElement)
              .value,
            phone: (document.getElementById("phone2") as HTMLInputElement)
              .value,
            country: isDifferentUniversity2
              ? (document.getElementById("memberCountry2") as HTMLSelectElement)
                  .value
              : (document.getElementById("country") as HTMLSelectElement).value,
            city: isDifferentUniversity2
              ? selectedCity2 === "Other"
                ? otherCity2
                : selectedCity2
              : selectedMainCity === "Other"
              ? otherMainCity
              : selectedMainCity,
            university: isDifferentUniversity2
              ? selectedUniversity2 === "Other"
                ? otherUniversity2
                : (
                    document.getElementById(
                      "memberUniversity2"
                    ) as HTMLSelectElement
                  ).options[
                    (
                      document.getElementById(
                        "memberUniversity2"
                      ) as HTMLSelectElement
                    ).selectedIndex
                  ].text
              : selectedMainUniversity === "Other"
              ? otherMainUniversity
              : universityName,
            isDifferentUniversity: isDifferentUniversity2,
          },
        ],
      };

      // Add optional team members only if they have data
      const firstName3Input = document.getElementById(
        "firstName3"
      ) as HTMLInputElement;
      if (firstName3Input?.value) {
        formData.teamMembers.push({
          type: "member3",
          firstName: firstName3Input.value,
          lastName: (document.getElementById("lastName3") as HTMLInputElement)
            .value,
          email: (document.getElementById("email3") as HTMLInputElement).value,
          phone: (document.getElementById("phone3") as HTMLInputElement).value,
          country: isDifferentUniversity3
            ? (document.getElementById("memberCountry3") as HTMLSelectElement)
                ?.value
            : (document.getElementById("country") as HTMLSelectElement).value,
          city: isDifferentUniversity3
            ? selectedCity3 === "Other"
              ? otherCity3
              : selectedCity3
            : selectedMainCity === "Other"
            ? otherMainCity
            : selectedMainCity,
          university: isDifferentUniversity3
            ? selectedUniversity3 === "Other"
              ? otherUniversity3
              : (
                  document.getElementById(
                    "memberUniversity3"
                  ) as HTMLSelectElement
                ).options[
                  (
                    document.getElementById(
                      "memberUniversity3"
                    ) as HTMLSelectElement
                  ).selectedIndex
                ].text
            : selectedMainUniversity === "Other"
            ? otherMainUniversity
            : universityName,
          isDifferentUniversity: isDifferentUniversity3,
        });
      }

      const firstName4Input = document.getElementById(
        "firstName4"
      ) as HTMLInputElement;
      if (firstName4Input?.value) {
        formData.teamMembers.push({
          type: "member4",
          firstName: firstName4Input.value,
          lastName: (document.getElementById("lastName4") as HTMLInputElement)
            .value,
          email: (document.getElementById("email4") as HTMLInputElement).value,
          phone: (document.getElementById("phone4") as HTMLInputElement).value,
          country: isDifferentUniversity4
            ? (document.getElementById("memberCountry4") as HTMLSelectElement)
                ?.value
            : (document.getElementById("country") as HTMLSelectElement).value,
          city: isDifferentUniversity4
            ? selectedCity4 === "Other"
              ? otherCity4
              : selectedCity4
            : selectedMainCity === "Other"
            ? otherMainCity
            : selectedMainCity,
          university: isDifferentUniversity4
            ? selectedUniversity4 === "Other"
              ? otherUniversity4
              : (
                  document.getElementById(
                    "memberUniversity4"
                  ) as HTMLSelectElement
                ).options[
                  (
                    document.getElementById(
                      "memberUniversity4"
                    ) as HTMLSelectElement
                  ).selectedIndex
                ].text
            : selectedMainUniversity === "Other"
            ? otherMainUniversity
            : universityName,
          isDifferentUniversity: isDifferentUniversity4,
        });
      }

      console.log("Sending form data:", formData);

      const response = await fetch("http://localhost:3001/api/submit-form", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log("Server response:", data);

      if (data.success) {
        alert("Form submitted successfully!");
        // Optionally reset form or redirect
      } else {
        throw new Error(data.message || "Error submitting form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Error submitting form. Please try again.");
    }
  };

  return (
    <FormWrapper>
      <FormTitle>The 2025 competitor registration form is now open!</FormTitle>

      <FormContainer onSubmit={handleSubmit}>
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
        <FormSelect id="country" name="country_code" required>
          <option value="">Country...</option>
          {countries.map((country) => (
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
          value={selectedMainCity}
          onChange={(e) =>
            handleSelectChange(
              e,
              handleCityChange,
              setSelectedMainCity,
              setOtherMainCity
            )
          }
        >
          <option value="">City...</option>
          {cities.map((city) => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
          <option value="Other">Other</option>
        </FormSelect>

        {selectedMainCity === "Other" && (
          <FormInput
            type="text"
            value={otherMainCity}
            onChange={(e) => setOtherMainCity(e.target.value)}
            placeholder="Enter city name"
            required
          />
        )}

        <FormLabel htmlFor="university">University *</FormLabel>
        <FormHint>
          If you do not see your university listed, scroll to the bottom and
          select "other"
        </FormHint>
        <FormSelect
          id="university"
          name="UniversityId__c"
          required
          value={selectedMainUniversity}
          onChange={(e) =>
            handleSelectChange(
              e,
              handleUniversityChange,
              setSelectedMainUniversity,
              setOtherMainUniversity
            )
          }
        >
          <option value="">University...</option>
          {universities.map((university) => (
            <option key={university.value} value={university.value}>
              {university.label}
            </option>
          ))}
        </FormSelect>

        {selectedMainUniversity === "Other" && (
          <FormInput
            type="text"
            value={otherMainUniversity}
            onChange={(e) => setOtherMainUniversity(e.target.value)}
            placeholder="Enter university name"
            required
          />
        )}

        {/* Team Captain Information */}
        <TeamMemberTitle>Team Member Information:</TeamMemberTitle>
        <ol>
          <li>
            <TeamMemberSubtitle>Team Captain Information</TeamMemberSubtitle>
            <TeamMemberHint>
              The team captain will be the main point of contact with Hult Prize
            </TeamMemberHint>
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
        <FormHint>
          Do not include any country codes, symbols, or spaces
        </FormHint>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "15px",
            margin: "0",
          }}
        >
          <FormSelect id="phoneCode" required style={{ width: "54%" }}>
            <option value="">Phone...</option>
            {phoneCodes.map((code) => (
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
            style={{ marginTop: "15px" }}
          />
          <input type="hidden" name="Phone" required />
        </div>

        <FormLabel htmlFor="differentUniversity1">
          Is this member of your team from a different University?
        </FormLabel>
        <FormHint>All members can be from a different university</FormHint>
        <CheckboxContainer>
          <input
            type="checkbox"
            id="differentUniversity1"
            name="Is_a_member_different_University__c"
            value="true"
            checked={isDifferentUniversity1}
            onChange={(e) => setIsDifferentUniversity1(e.target.checked)}
          />
          <span>Yes</span>
        </CheckboxContainer>

        {isDifferentUniversity1 && (
          <>
            <FormLabel htmlFor="memberCountry1">Country *</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect
              id="memberCountry1"
              name="member_country"
              required={isDifferentUniversity1}
              value={selectedCountry1}
              onChange={(e) => setSelectedCountry1(e.target.value)}
            >
              <option value="">Country...</option>
              {countries.map((country) => (
                <option key={country.value} value={country.value}>
                  {country.label}
                </option>
              ))}
            </FormSelect>

            <FormLabel htmlFor="memberCity1">City *</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect
              id="memberCity1"
              name="member_city"
              required={isDifferentUniversity1}
              value={selectedCity1}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleCityChange,
                  setSelectedCity1,
                  setOtherCity1
                )
              }
            >
              <option value="">City...</option>
              {cities.map((city) => (
                <option key={city.value} value={city.value}>
                  {city.label}
                </option>
              ))}
              <option value="Other">Other</option>
            </FormSelect>

            {selectedCity1 === "Other" && (
              <FormInput
                type="text"
                value={otherCity1}
                onChange={(e) => setOtherCity1(e.target.value)}
                placeholder="Enter city name"
                required={isDifferentUniversity1}
              />
            )}

            <FormLabel htmlFor="memberUniversity1">University *</FormLabel>
            <FormHint>
              If you do not see your university listed, scroll to the bottom and
              select "other"
            </FormHint>
            <FormSelect
              id="memberUniversity1"
              name="member_university"
              required={isDifferentUniversity1}
              value={selectedUniversity1}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleUniversityChange,
                  setSelectedUniversity1,
                  setOtherUniversity1
                )
              }
            >
              <option value="">University...</option>
              {universities.map((university) => (
                <option key={university.value} value={university.value}>
                  {university.label}
                </option>
              ))}
              <option value="Other">Other</option>
            </FormSelect>

            {selectedUniversity1 === "Other" && (
              <FormInput
                type="text"
                value={otherUniversity1}
                onChange={(e) => setOtherUniversity1(e.target.value)}
                placeholder="Enter university name"
                required={isDifferentUniversity1}
              />
            )}
          </>
        )}

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
        <FormHint>
          Do not include any country codes, symbols, or spaces
        </FormHint>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "15px",
            margin: "0",
          }}
        >
          <FormSelect
            id="phoneCode2"
            required
            style={{ width: "54%", marginRight: "15px" }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map((code) => (
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
            style={{ marginTop: "15px" }}
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
            checked={isDifferentUniversity2}
            onChange={(e) => setIsDifferentUniversity2(e.target.checked)}
          />
          <span>Yes</span>
        </CheckboxContainer>

        {isDifferentUniversity2 && (
          <>
            <FormLabel htmlFor="memberCountry2">Country *</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect id="memberCountry2" name="member_country2" required>
              <option value="">Country...</option>
              {countries.map((country) => (
                <option key={country.value} value={country.value}>
                  {country.label}
                </option>
              ))}
            </FormSelect>

            <FormLabel htmlFor="memberCity2">City *</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect
              id="memberCity2"
              name="member_city2"
              required
              value={selectedCity2}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleCityChange,
                  setSelectedCity2,
                  setOtherCity2
                )
              }
            >
              <option value="">City...</option>
              {cities.map((city) => (
                <option key={city.value} value={city.value}>
                  {city.label}
                </option>
              ))}
              <option value="Other">Other</option>
            </FormSelect>

            {selectedCity2 === "Other" && (
              <FormInput
                type="text"
                value={otherCity2}
                onChange={(e) => setOtherCity2(e.target.value)}
                placeholder="Enter city name"
                required
              />
            )}

            <FormLabel htmlFor="memberUniversity2">University *</FormLabel>
            <FormHint>
              If you do not see your university listed, scroll to the bottom and
              select "other"
            </FormHint>
            <FormSelect
              id="memberUniversity2"
              name="member_university2"
              required
              value={selectedUniversity2}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleUniversityChange,
                  setSelectedUniversity2,
                  setOtherUniversity2
                )
              }
            >
              <option value="">University...</option>
              {universities.map((university) => (
                <option key={university.value} value={university.value}>
                  {university.label}
                </option>
              ))}
            </FormSelect>

            {selectedUniversity2 === "Other" && (
              <FormInput
                type="text"
                value={otherUniversity2}
                onChange={(e) => setOtherUniversity2(e.target.value)}
                placeholder="Enter university name"
                required
              />
            )}
          </>
        )}

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
        <FormHint>
          Do not include any country codes, symbols, or spaces
        </FormHint>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "15px",
            margin: "0",
          }}
        >
          <FormSelect
            id="phoneCode3"
            style={{ width: "54%", marginRight: "15px" }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map((code) => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone3"
            type="tel"
            pattern="[0-9.]+"
            style={{ marginTop: "15px" }}
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
            checked={isDifferentUniversity3}
            onChange={(e) => setIsDifferentUniversity3(e.target.checked)}
          />
          <span>Yes</span>
        </CheckboxContainer>

        {isDifferentUniversity3 && (
          <>
            <FormLabel htmlFor="memberCountry3">Country</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect id="memberCountry3" name="member_country3">
              <option value="">Country...</option>
              {countries.map((country) => (
                <option key={country.value} value={country.value}>
                  {country.label}
                </option>
              ))}
            </FormSelect>

            <FormLabel htmlFor="memberCity3">City</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect
              id="memberCity3"
              name="member_city3"
              value={selectedCity3}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleCityChange,
                  setSelectedCity3,
                  setOtherCity3
                )
              }
            >
              <option value="">City...</option>
              {cities.map((city) => (
                <option key={city.value} value={city.value}>
                  {city.label}
                </option>
              ))}
              <option value="Other">Other</option>
            </FormSelect>

            {selectedCity3 === "Other" && (
              <FormInput
                type="text"
                value={otherCity3}
                onChange={(e) => setOtherCity3(e.target.value)}
                placeholder="Enter city name"
              />
            )}

            <FormLabel htmlFor="memberUniversity3">University</FormLabel>
            <FormHint>
              If you do not see your university listed, scroll to the bottom and
              select "other"
            </FormHint>
            <FormSelect
              id="memberUniversity3"
              name="member_university3"
              value={selectedUniversity3}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleUniversityChange,
                  setSelectedUniversity3,
                  setOtherUniversity3
                )
              }
            >
              <option value="">University...</option>
              {universities.map((university) => (
                <option key={university.value} value={university.value}>
                  {university.label}
                </option>
              ))}
            </FormSelect>

            {selectedUniversity3 === "Other" && (
              <FormInput
                type="text"
                value={otherUniversity3}
                onChange={(e) => setOtherUniversity3(e.target.value)}
                placeholder="Enter university name"
              />
            )}
          </>
        )}

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
        <FormHint>
          Do not include any country codes, symbols, or spaces
        </FormHint>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "15px",
            margin: "0",
          }}
        >
          <FormSelect
            id="phoneCode4"
            style={{ width: "54%", marginRight: "15px" }}
          >
            <option value="">Phone...</option>
            {phoneCodes.map((code) => (
              <option key={code.value} value={code.value}>
                {code.label}
              </option>
            ))}
          </FormSelect>
          <FormInput
            id="phone4"
            type="tel"
            pattern="[0-9.]+"
            style={{ marginTop: "15px" }}
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
            checked={isDifferentUniversity4}
            onChange={(e) => setIsDifferentUniversity4(e.target.checked)}
          />
          <span>Yes</span>
        </CheckboxContainer>

        {isDifferentUniversity4 && (
          <>
            <FormLabel htmlFor="memberCountry4">Country</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect id="memberCountry4" name="member_country4">
              <option value="">Country...</option>
              {countries.map((country) => (
                <option key={country.value} value={country.value}>
                  {country.label}
                </option>
              ))}
            </FormSelect>

            <FormLabel htmlFor="memberCity4">City</FormLabel>
            <FormHint>Where your university is located</FormHint>
            <FormSelect
              id="memberCity4"
              name="member_city4"
              value={selectedCity4}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleCityChange,
                  setSelectedCity4,
                  setOtherCity4
                )
              }
            >
              <option value="">City...</option>
              {cities.map((city) => (
                <option key={city.value} value={city.value}>
                  {city.label}
                </option>
              ))}
              <option value="Other">Other</option>
            </FormSelect>

            {selectedCity4 === "Other" && (
              <FormInput
                type="text"
                value={otherCity4}
                onChange={(e) => setOtherCity4(e.target.value)}
                placeholder="Enter city name"
                required
              />
            )}

            <FormLabel htmlFor="memberUniversity4">University</FormLabel>
            <FormHint>
              If you do not see your university listed, scroll to the bottom and
              select "other"
            </FormHint>
            <FormSelect
              id="memberUniversity4"
              name="member_university4"
              value={selectedUniversity4}
              onChange={(e) =>
                handleSelectChange(
                  e,
                  handleUniversityChange,
                  setSelectedUniversity4,
                  setOtherUniversity4
                )
              }
            >
              <option value="">University...</option>
              {universities.map((university) => (
                <option key={university.value} value={university.value}>
                  {university.label}
                </option>
              ))}
            </FormSelect>

            {selectedUniversity4 === "Other" && (
              <FormInput
                type="text"
                value={otherUniversity4}
                onChange={(e) => setOtherUniversity4(e.target.value)}
                placeholder="Enter university name"
              />
            )}
          </>
        )}

        <FormLabel htmlFor="sdg">
          Sustainable Development Goal (SDG) *
        </FormLabel>
        <FormHint>
          Select the main Sustainable Development Goal (SDG) your startup will
          align with
        </FormHint>
        <FormSelect id="sdg" name="Sustainable_Development_Goals__c" required>
          <option value="">Sustainable Development Goal (SDG)...</option>
          {sdgs.map((sdg) => (
            <option key={sdg.value} value={sdg.value}>
              {sdg.label}
            </option>
          ))}
        </FormSelect>

        {/* Previous Experience Checkboxes */}
        <FormLabel htmlFor="experience">
          Previous Hult Prize experience
        </FormLabel>
        <FormHint>Check all that apply</FormHint>
        <CheckboxContainer>
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="competitor"
              name="HP_History__c"
              value="Competitor"
            />
            <span>Competitor</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="volunteer"
              name="HP_History__c"
              value="Global Event Volunteer"
            />
            <span>Global Event Volunteer</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="firstTime"
              name="HP_History__c"
              value="First Time Hearing About HP"
            />
            <span>First Time Hearing About HP</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="onCampus"
              name="HP_History__c"
              value="OnCampus Program Volunteer"
            />
            <span>OnCampus Program Volunteer</span>
          </div>
        </CheckboxContainer>

        {/* How did you find out about Hult Prize */}
        <FormLabel htmlFor="findOut">
          How did you find out about Hult Prize? *
        </FormLabel>
        <CheckboxContainer>
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="countryCoordinator"
              name="LeadSource"
              value="Country Coordinator"
              required
            />
            <span>Country Coordinator</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="friend"
              name="LeadSource"
              value="Friend"
              required
            />
            <span>Friend</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="hultAlumni"
              name="LeadSource"
              value="Hult Prize Alumni"
              required
            />
            <span>Hult Prize Alumni</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="campusDirector"
              name="LeadSource"
              value="Hult Prize Campus Director"
              required
            />
            <span>Hult Prize Campus Director</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="directComm"
              name="LeadSource"
              value="Hult Prize Team - Direct Communication"
              required
            />
            <span>Hult Prize Team - Direct Communication</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="website"
              name="LeadSource"
              value="Hult Prize Website"
              required
            />
            <span>Hult Prize Website</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="internetSearch"
              name="LeadSource"
              value="Internet Search"
              required
            />
            <span>Internet Search</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="facebookSocial"
              name="LeadSource"
              value="Social Media - Facebook"
              required
            />
            <span>Social Media - Facebook</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="instagramSocial"
              name="LeadSource"
              value="Social Media - Instagram"
              required
            />
            <span>Social Media - Instagram</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="linkedinSocial"
              name="LeadSource"
              value="Social Media - LinkedIn"
              required
            />
            <span>Social Media - LinkedIn</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="otherSocial"
              name="LeadSource"
              value="Social Media - Other"
              required
            />
            <span>Social Media - Other</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="universityRep"
              name="LeadSource"
              value="University Rep"
              required
            />
            <span>University Rep</span>
          </div>

          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="radio"
              id="other"
              name="LeadSource"
              value="Other"
              required
            />
            <span>Other</span>
          </div>
        </CheckboxContainer>

        {/* Team Confirmation */}
        <FormLabel htmlFor="teamConfirmation">
          You confirm that your team consists of 2-4 currently enrolled
          students, all of whom are aged 18 or older by February 28th, 2025. *
        </FormLabel>
        <CheckboxContainer>
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="teamConfirmation"
              name="team_confirmation"
              required
            />
            <span>I confirm</span>
          </div>
        </CheckboxContainer>

        {/* Terms and Conditions */}
        <FormLabel htmlFor="termsConditions">Accept T&Cs *</FormLabel>
        <CheckboxContainer>
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="termsConditions"
              name="terms_conditions"
              required
            />
            <span>I agree to the Hult Prize terms and conditions</span>
          </div>
        </CheckboxContainer>

        <SubmitButton type="submit">Apply Now!</SubmitButton>
      </FormContainer>
    </FormWrapper>
  );
};

export default RegistrationForm;
